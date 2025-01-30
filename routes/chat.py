import os
import base64
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from models import db, ChatBot, ChatHistory
from cohere_test import generate_response

chat_bp = Blueprint('chat', __name__)

UPLOAD_FOLDER = 'static/profile_pics/'  # Folder to store profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@chat_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_bot():
    if request.method == 'POST':
        try:
            name = request.form['name']
            personality = request.form['personality']
            is_public = 'is_public' in request.form
            profile_pic = None

            # Handle profile picture upload (Base64 or File)
            if 'cropped_image' in request.form and request.form['cropped_image']:
                # Decode Base64 image and save it
                img_data = request.form['cropped_image'].split(
                    ',')[1]  # Remove "data:image/png;base64,"
                filename = secure_filename(
                    f"{name.lower().replace(' ', '_')}.png")
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(img_data))
                profile_pic = file_path  # Store file path in DB

            new_bot = ChatBot(
                name=name,
                personality=personality,
                is_public=is_public,
                profile_pic=profile_pic,
                user_id=current_user.id
            )
            db.session.add(new_bot)
            db.session.commit()
            flash('Bot created successfully!', 'success')
            return redirect(url_for('list.home'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating bot', 'danger')
    return render_template('create.html')


@chat_bp.route('/edit/<int:bot_id>', methods=['POST'])
@login_required
def edit_bot(bot_id):
    bot = ChatBot.query.get_or_404(bot_id)

    # Ensure only the bot owner can edit
    if bot.user_id != current_user.id:
        flash("You don't have permission to edit this bot.", "danger")
        return redirect(url_for('chat.chat_interface', bot_id=bot_id))

    bot.name = request.form['name']
    bot.personality = request.form['personality']

    # Handle profile picture update
    if 'cropped_image' in request.form and request.form['cropped_image']:
        img_data = request.form['cropped_image'].split(',')[1]
        filename = secure_filename(f"{bot.name.lower().replace(' ', '_')}.png")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(img_data))
        bot.profile_pic = file_path

    db.session.commit()
    flash("Bot updated successfully!", "success")
    return redirect(url_for('chat.chat_interface', bot_id=bot.id))


@chat_bp.route('/chat/<int:bot_id>')
@login_required
def chat_interface(bot_id):
    bot = ChatBot.query.get_or_404(bot_id)
    history = ChatHistory.query.filter_by(
        user_id=current_user.id,
        bot_id=bot_id
    ).order_by('timestamp').all()

    return render_template('chat.html', bot=bot, history=history)


@chat_bp.route('/send/<int:bot_id>', methods=['POST'])
@login_required
def send_message(bot_id):
    bot = ChatBot.query.get_or_404(bot_id)
    user_input = request.form['message']

    # If this is the first message, don't store "Please introduce yourself"
    history = ChatHistory.query.filter_by(
        user_id=current_user.id,
        bot_id=bot_id
    ).order_by('timestamp').all()

    # Generate response
    bot_response = generate_response(
        bot.name, bot.personality, user_input, history)
    print("Bot Response:", bot_response)

    # Store interaction
    new_chat = ChatHistory(
        user_id=current_user.id,
        bot_id=bot_id,
        message=user_input,
        response=bot_response
    )
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({'response': bot_response})


@chat_bp.route('/delete/<int:bot_id>', methods=['POST'])
@login_required
def delete_bot(bot_id):
    bot = ChatBot.query.get_or_404(bot_id)

    # Ensure only the bot owner can delete
    if bot.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(bot)
    db.session.commit()
    return jsonify({"success": True})

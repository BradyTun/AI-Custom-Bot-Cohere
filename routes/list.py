from flask import Blueprint, render_template
from flask_login import current_user, login_required
from models import ChatBot

list_bp = Blueprint('list', __name__)

@list_bp.route('/')
@login_required
def home():
    user_bots = ChatBot.query.filter_by(user_id=current_user.id).all()
    public_bots = ChatBot.query.filter_by(is_public=True)\
        .filter(ChatBot.user_id != current_user.id).all()
    return render_template('list.html', 
                         user_bots=user_bots,
                         public_bots=public_bots)
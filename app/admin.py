from app.models import Category, Product, UserRoleEnum
from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, render_template


admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyProductView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'price', 'active']
    column_searchable_list = ['name']
    column_filters = ['name', 'price']
    column_editable_list = ['name', 'price']
    create_modal = True
    edit_modal = True


class MyCategoryView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'products']


class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

class Book(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/book.html')

class QuiDinh(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/rule.html')

admin.add_view(Book(name='Nhập sách'))
admin.add_view(QuiDinh(name='Quy định'))
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(StatsView(name='Thông kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))


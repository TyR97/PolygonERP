from datetime import datetime

from flask import flash, render_template, request, Blueprint, redirect, url_for
from sqlalchemy.dialects.oracle.dictionary import all_users
from sqlalchemy.exc import SQLAlchemyError
from polygonerp.db import db
from polygonerp.forms.edit_project_form import UpdateProjectForm
from polygonerp.models.project import Project
from polygonerp.models.user import User
from polygonerp.utils.decorators_util import admin_required, login_required
from polygonerp.forms.delete_project_form import DeleteProjectForm


class ProjectController:

    def __init__(self, blueprint, app):
        self.bp = blueprint
        self.bp.add_url_rule('/', view_func=login_required(self.project_dash), methods=['GET', 'POST'])
        self.bp.add_url_rule('/project/<project_id>', view_func=login_required(self.project_detail), methods=['GET', 'POST'])
        self.bp.add_url_rule('/create', view_func=admin_required(self.create_project), methods=['GET', 'POST'])
        self.bp.add_url_rule('/list_projects', view_func=self.list_projects, methods=['GET', 'POST'])
        self.bp.add_url_rule('/delete/<project_id>', view_func=admin_required(self.delete_project), methods=['GET', 'POST'])
        self.bp.add_url_rule('/edit/<project_id>', view_func=admin_required(self.edit_project),methods=['GET', 'POST'])


    def project_dash(self):
        return render_template('project/project_dash.html')

    def project_detail(self, project_id):
        project = Project.query.get(project_id)

        return render_template('project/project_detail.html', project=project)


    def create_project(self):
        all_users = User.query.all()
        if request.method == 'POST':

            try:

                name = request.form['name']
                start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
                finish_date = datetime.strptime(request.form['finish_date'], "%Y-%m-%d").date()
                supervisor_id = request.form['supervisor_id']
                worker_ids = request.form.getlist('workers')
                supervisor = db.session.get(User, supervisor_id)
                workers = [db.session.get(User, int(uid)) for uid in worker_ids]

                new_project = Project(
                        name=name,
                        start_date=start_date,
                        finish_date=finish_date,
                        supervisor=supervisor,
                        assigned_workers=workers
                    )

                if start_date > finish_date:
                    flash("Start date cannot be later than finish date.", "danger")
                    return render_template("project/create_project.html", supervisors=all_users, workers=workers)

                db.session.add(new_project)
                db.session.commit()
                return redirect(url_for('project.list_projects'))

            except SQLAlchemyError as e:
                 db.session.rollback()
                 flash("Error creating project: " + str(e), "danger")


        return render_template('project/create_project.html', supervisors=all_users, workers=all_users)

    def list_projects(self):
        projects = Project.query.all()
        if not projects:
            flash("No projects found!", "danger")
        return render_template('project/list_projects.html', projects=projects)

    def edit_project(self, project_id):
        project = Project.query.get_or_404(project_id)
        form = UpdateProjectForm(obj=project)
        form.populate_supervisor_choices()
        if form.validate_on_submit():
            form.populate_obj(project)
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                flash("Error updating project: " + str(e), "danger")
                db.session.rollback()
            else:
                flash("Project updated successfully!", "success")
                return redirect(url_for('project.list_projects'))
        return render_template('project/edit_project.html', form=form, project=project)

    def delete_project(self, project_id):
        project = Project.query.get(project_id)
        form = DeleteProjectForm()

        if not project:
                flash("Project not found!", "danger")
        else:
            if form.validate_on_submit():
                try:
                        db.session.delete(project)
                        db.session.commit()
                except SQLAlchemyError as e:
                        db.session.rollback()
                        print(e)
                else:
                        return redirect(url_for('project.list_projects'))

        return render_template('project/delete_project.html', project_id=project_id, form=form)


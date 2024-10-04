# src/controllers/rca_controller.py
from itertools import product
from flask import render_template, request, redirect, session, url_for, flash
from sqlalchemy import desc
from models.rca_models import DocumentActionHistory, IncidentSeverity, RCADocument, RootCause, User, db
from datetime import datetime

class RCAController:
    
    @staticmethod
    def rca_list():
        DEFAULT_PER_PAGE = 10
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)
        rcas = RCADocument.query.paginate(page=page, per_page=per_page)
        return render_template('rca_list.html', rcas=rcas, per_page=per_page)

    @staticmethod
    def create_rca():
        if request.method == 'POST':
            try:
                # Convertir les champs de date et de temps depuis les chaînes de caractères du formulaire
                incident_date = datetime.strptime(request.form['incident_date'], '%Y-%m-%d').date() if request.form.get('incident_date') else None
                incident_time = datetime.strptime(request.form['incident_time'], '%H:%M').time() if request.form.get('incident_time') else None
                reported_date = datetime.strptime(request.form['reported_date'], '%Y-%m-%d').date() if request.form.get('reported_date') else None
                restored_date = datetime.strptime(request.form['restored_date'], '%Y-%m-%d').date() if request.form.get('restored_date') else None
                rca_submission_date = datetime.strptime(request.form['rca_submission_date'], '%Y-%m-%d').date() if request.form.get('rca_submission_date') else None
                
                # Gérer la durée de l'impact de service (sous forme de texte)
                service_impact_duration_value = request.form.get('service_impact_duration_value', '')
                service_impact_duration_unit = request.form.get('service_impact_duration_unit', '')

                # Combiner la valeur et l'unité pour obtenir une chaîne de caractères
                service_impact_duration = f"{service_impact_duration_value} {service_impact_duration_unit}" if service_impact_duration_value and service_impact_duration_unit else None

                # Récupérer l'ID de l'utilisateur connecté depuis la session
                created_by = session.get('user_id')

                # Créer le nouvel objet RCA
                new_rca = RCADocument(
                    incident_number=request.form['incident_number'],
                    customer_name=request.form['customer_name'],
                    product_name=request.form['product_name'],
                    product_version=request.form['product_version'],
                    incident_date=incident_date,
                    incident_time=incident_time,
                    reported_date=reported_date,
                    restored_date=restored_date,
                    rca_report_status=request.form['rca_report_status'],
                    rca_submission_date=rca_submission_date,
                    problem_category=request.form['problem_category'],
                    problem_sub_category=request.form['problem_sub_category'],
                    service_impact=request.form['service_impact'],
                    service_impact_duration=service_impact_duration,  # Stocké sous forme de texte
                    incident_impact=request.form['incident_impact'],
                    current_status=request.form['current_status'],
                    problem_statement=request.form['problem_statement'],
                    way_forward=request.form['way_forward'],
                    incident_severity_id=request.form['incident_severity_id'],
                    created_by=created_by if created_by else None  # Gestion de l'utilisateur connecté
                )
                # Historiser l'action
                action_history = DocumentActionHistory(
                    rca_document_id=new_rca.id,
                    action="Created RCA Document",
                    performed_by=created_by if created_by else None
                )
                db.session.add(action_history)
                # Ajouter et commit dans la base de données
                db.session.add(new_rca)
                db.session.commit()

                flash('RCA document created successfully', 'success')
                return redirect(url_for('rca.rca_list'))
            
            except ValueError as e:
                # En cas d'erreur de formatage des dates ou des heures
                flash(f"Invalid date or time format: {str(e)}", 'danger')
                return redirect(url_for('rca.create_rca'))

        # Récupérer toutes les sévérités d'incidents
        severities = IncidentSeverity.query.all()
        return render_template('rca_form.html', rca=None, severities=severities)

    @staticmethod
    def view_rca(rca_id):
        rca = RCADocument.query.get_or_404(rca_id)

        if rca.service_impact_duration:
            duration_parts = rca.service_impact_duration.split(' ')
            service_impact_duration_value = duration_parts[0]
            service_impact_duration_unit = duration_parts[1] if len(duration_parts) > 1 else ''
        else:
            service_impact_duration_value = ''
            service_impact_duration_unit = ''
        
        # Récupérer toutes les sévérités d'incidents
        severities = IncidentSeverity.query.all()
        return render_template('rca_form.html', rca=rca, view_only=True, severities=severities, service_impact_duration_value=service_impact_duration_value, service_impact_duration_unit=service_impact_duration_unit)

    @staticmethod
    def edit_rca(rca_id):
        rca = RCADocument.query.get_or_404(rca_id)
        if request.method == 'POST':
            try:
                # Mettre à jour les champs de base
                rca.incident_number = request.form['incident_number']
                rca.customer_name = request.form['customer_name']
                rca.product_name = request.form['product_name']
                rca.product_version = request.form['product_version']
                rca.incident_date = datetime.strptime(request.form['incident_date'], '%Y-%m-%d').date() if request.form.get('incident_date') else None
                rca.incident_time = datetime.strptime(request.form['incident_time'], '%H:%M:%S').time() if request.form.get('incident_time') else None  # Modifié ici
                rca.reported_date = datetime.strptime(request.form['reported_date'], '%Y-%m-%d').date() if request.form.get('reported_date') else None
                rca.restored_date = datetime.strptime(request.form['restored_date'], '%Y-%m-%d').date() if request.form.get('restored_date') else None
                rca.rca_report_status = request.form['rca_report_status']
                rca.problem_category = request.form['problem_category']
                rca.problem_sub_category = request.form['problem_sub_category']
                rca.service_impact = request.form['service_impact']
                
                # Gérer la durée de l'impact de service (sous forme de texte)
                service_impact_duration_value = request.form.get('service_impact_duration_value', '')
                service_impact_duration_unit = request.form.get('service_impact_duration_unit', '')

                # Combiner la valeur et l'unité pour obtenir une chaîne de caractères
                rca.service_impact_duration = f"{service_impact_duration_value} {service_impact_duration_unit}" if service_impact_duration_value and service_impact_duration_unit else None
                
                # Mettre à jour les autres champs
                rca.incident_impact = request.form['incident_impact']
                rca.current_status = request.form['current_status']
                rca.problem_statement = request.form['problem_statement']
                rca.way_forward = request.form['way_forward']
                rca.incident_severity_id = request.form['incident_severity_id']

                # Historiser l'action de modification
                action_history = DocumentActionHistory(
                    rca_document_id=rca.id,
                    action="Updated RCA Document",
                    performed_by=session.get('user_id')
                )
                db.session.add(action_history)

                db.session.commit()
                flash('RCA document updated successfully', 'success')
                return redirect(url_for('rca.rca_list'))

            except ValueError as e:
                flash(f"Invalid date or time format: {str(e)}", 'danger')
                return redirect(url_for('rca.edit_rca', rca_id=rca_id))
            
        # Extraire la valeur et l'unité pour l'affichage
        if rca.service_impact_duration:
            duration_parts = rca.service_impact_duration.split(' ')
            service_impact_duration_value = duration_parts[0]
            service_impact_duration_unit = duration_parts[1] if len(duration_parts) > 1 else ''
        else:
            service_impact_duration_value = ''
            service_impact_duration_unit = ''

        # Récupérer toutes les sévérités d'incidents
        severities = IncidentSeverity.query.all()
        return render_template('rca_form.html', rca=rca, severities=severities, service_impact_duration_value=service_impact_duration_value, service_impact_duration_unit=service_impact_duration_unit)


    @staticmethod
    def add_root_cause(rca_id):
        if request.method == 'POST':
            new_root_cause = RootCause(
                rca_document_id=rca_id,
                description=request.form['description']
            )
            db.session.add(new_root_cause)
            db.session.commit()
            flash('Root cause added successfully', 'success')
        return redirect(url_for('rca.edit_rca', rca_id=rca_id))
    
    @staticmethod
    def delete_root_cause(root_cause_id):
        root_cause = RootCause.query.get_or_404(root_cause_id)
        rca_id = root_cause.rca_document_id
        db.session.delete(root_cause)
        db.session.commit()
        flash('Root cause deleted successfully', 'success')
        return redirect(url_for('rca.edit_rca', rca_id=rca_id))
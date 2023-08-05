# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import request
from flask.ext.login import login_required, current_user
from onyx.decorators import admin_required
from .. import api
import json
from onyx.api.calendar import *
from onyx.api.exceptions import *

events = Calendar()

@api.route('calendar', methods=['GET','POST','PUT'])
@login_required
@admin_required
def calendars():
	if request.method == 'GET':
		"""
		@api {get} /calendar Request Events Information
		@apiName getEvent
		@apiGroup Calendar
		@apiPermission authenticated

		@apiSuccess (200) {Object[]} events List of Event
		@apiSuccess (200) {Number} events.id Id of Event
		@apiSuccess (200) {String} events.title Title of Event
		@apiSuccess (200) {String} events.notes Notes of Event
		@apiSuccess (200) {String} events.lieu Place of Event
		@apiSuccess (200) {datetime} events.start Start date of Event
		@apiSuccess (200) {datetime} events.stop Stop date of Event
		@apiSuccess (200) {String} events.color Color of Event

		@apiError EventNotFound No Event Found

		"""
		try:
			events.user = current_user.id
			return events.get()
		except CalendarException as e:
			return "Error : " + e

	elif request.method == 'POST':
		"""
		@api {post} /calendar Add Event
		@apiName addEvent
		@apiGroup Calendar
		@apiPermission authenticated

		@apiParam {String} title Title of Event
		@apiParam {String} notes Notes of Event
		@apiParam {String} lieu Place of Event
		@apiParam {datetime} start Start date of Event
		@apiParam {datetime} stop Stop date of Event
		@apiParam {String} color Color of Event

		@apiSuccess (200) redirect Redirect to Calendar

		@apiError AlreadyExist This Event already Exist

		"""
		try:
			events.user = current_user.id
			events.title = request.form['title']
			events.notes = request.form['notes']
			events.lieu = request.form['lieu']
			events.color = request.form['color']
			events.startdate = request.form['start']
			events.enddate = request.form['end']
			return events.add()
		except CalendarException as e:
			return 'Error : ' + e

	elif request.method == 'PUT':
		"""
		@api {patch} /calendar Update Date
		@apiName updateEvent
		@apiGroup Calendar
		@apiPermission authenticated

		@apiParam {datetime} start Start date of Event
		@apiParam {datetime} stop Stop date of Event

		@apiSuccess (200) {json} status Status of Update

		@apiError {json} status An error has occurred

		"""
		try:
			events.user = current_user.id
			events.id = request.form['id']
			events.startdate = request.form['start']
			events.enddate = request.form['end']
			return events.update_date()
		except CalendarException as e:
			return 'Error : ' + str(e)

@api.route('calendar/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def calendar(id):
	if request.method == 'POST':
		"""
		@api {put} /calendar/:id Update Event
		@apiName updateEvent
		@apiGroup Calendar
		@apiPermission authenticated

		@apiParam {boolean} delete Delete an Event
		@apiParam {String} title Title of Event
		@apiParam {String} notes Notes of Event
		@apiParam {String} lieu Place of Event
		@apiParam {String} color Color of Event

		@apiSuccess (200) redirect Redirect to Calendar

		@apiError AlreadyExist This Event already Exist

		"""
		try:
			checked = 'delete' in request.form
			if checked == True:
				events.user = current_user.id
				events.id = request.form['id']
				events.delete()
			events.user = current_user.id
			events.id = request.form['id']
			events.title = request.form['title']
			events.notes = request.form['notes']
			events.lieu = request.form['lieu']
			events.color = request.form['color']

			return events.update_event()
		except CalendarException as e:
			return 'Error : ' + e

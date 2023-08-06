satmetrix
=========

Usage::

    from satmetrix import Satmetrix
	sm = Satmetrix(domain, auth)


Retrieve one page of feedback::

	data = sm.feedback(page_limit=1)
	contact_id = data[0]['contact_record_id']

Retrieve one feedback record using contact_record_id::

	r = sm.feedback_record(contact_id)

Update feedback record::

	r = sm.update_feedback(contact_record_id, data=[{'contact_record_id': contact_record_id, 'comment_text': 'Called customer, left vm. Will call back to cust next week.'}])

Retrieve invitation record using contact_record_id::

	r = sm.invitation_record(contact_record_id)

Nominate Contact::

	r = sm.nominate_contact(data=[{'contact_id': 'email', 'email': 'email'}])
	r = sm.nominate_contact(contact_record_id)

The above will return all the feedback you have. You can pass in the following arguments offset, limit, page_limit, callback. You can also pass in additional args which are passed to as json data in the post request.

Note
~~~~
Satmetrix has said there isn't an endpoint other than searching.

import maya

class TimestampHandler:

    def turn_timestamp_into_age(self, sessions):
        # age to znormalizowana różnica między aktualnym timestampem, a najwcześniejszym
        # timestampem dla każdego użytkownika
        sessions = self._add_age_column(sessions)
        sessions = self._drop(sessions, 'timestamp')
        return sessions

    def _drop(self, sessions, to_drop):
        for session in sessions:
                session.pop(to_drop)
        return sessions

    def _add_age_column(self, sessions):
        first, last = self._find_edge_entries_for_every_user(sessions)
        sessions = self._calculate_age_from_timestamp(sessions, first, last)
        return sessions
    
    def _calculate_age_from_timestamp(self, sessions, first, last):    
        for session in sessions:
            date = maya.parse(session['timestamp']).datetime()
            # if last is first, there is only one entry
            if last[session['user_id']] == first[session['user_id']]:
                session['age'] = 1
            else:
                session['age'] = (date - first[session['user_id']]) / (last[session['user_id']] - first[session['user_id']])
        return sessions

    def _find_edge_entries_for_every_user(self, sessions):
        # przechowuje najnowsze i najstarsze wejscie dla kazdego uzytkownika
        first_entries = {}
        last_entries = {}
        for session in sessions:
            current_date = maya.parse(session['timestamp']).datetime()
            current_user_id = session['user_id']

            first_entries[current_user_id] = self._find_minimising_value(first_entries, current_user_id, current_date)
            last_entries[current_user_id] = self._find_maximising_value(last_entries, current_user_id, current_date)

        return first_entries, last_entries
    
    def _find_minimising_value(self, first_entries, current_user_id, current_date):
        return min(first_entries[current_user_id], current_date) if current_user_id in first_entries else current_date

    def _find_maximising_value(self, last_entries, current_user_id, current_date):
        return max(last_entries[current_user_id], current_date) if current_user_id in last_entries else current_date

class UserIdFiller:

    def fill_missing_user_id_where_possible(self, sessions):
        for i, session in enumerate(sessions):
            if session['user_id'] is None:
                # ustaw wartosc sesji na podstawie sasiadow
                session['user_id'] = self._find_user_id_from_neighbours(sessions, i)
        return sessions

    def _find_user_id_from_neighbours(self, sessions, i):
        prev_not_null_user_id, prev_not_null_session_id = self._get_prev_not_null_user_and_session_id(sessions, i)
        next_not_null_user_id, next_not_null_session_id = self._get_next_not_null_user_and_session_id(sessions, i)

        # jezeli poprzedni rekord ma taki sam user_id jak nastepny, to wpisz ten user_id
        if prev_not_null_user_id == next_not_null_user_id:
            return next_not_null_user_id
        # jezeli id sesji poprzedniego rekordu jest takie samo, to znaczy, ze musi to byc ten sam user_id
        if prev_not_null_session_id == sessions[i]['session_id']:
            return prev_not_null_user_id 
        # jezeli id sesji nastepnego rekordu jest takie samo, to znaczy, ze musi byc to ten sam user_id
        if next_not_null_session_id == sessions[i]['session_id']:
            return next_not_null_user_id 
        
        return None

    def _get_prev_not_null_user_and_session_id(self, sessions, i):
        while i >= 0 and sessions[i]['user_id'] is None:
            i -= 1
        return sessions[i]['user_id'], sessions[i]['session_id']

    def _get_next_not_null_user_and_session_id(self, sessions, i):
        while i < len(sessions) and sessions[i]['user_id'] is None:
            i += 1
        return sessions[i]['user_id'], sessions[i]['session_id']

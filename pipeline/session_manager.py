import time
import uuid


class SessionManager:

    def __init__(self):
        # permanent identity mapping (CORE FIX)
        self.track_to_visitor = {}

        # session state per track_id
        self.sessions = {}

    def get_or_create_session(self, track_id):

        now = time.time()

        # ---------------------------------------
        # STEP 1: FIXED IDENTITY (OPTION A CORE)
        # ---------------------------------------
        if track_id not in self.track_to_visitor:
            self.track_to_visitor[track_id] = f"VIS_{uuid.uuid4().hex[:8]}"

        visitor_id = self.track_to_visitor[track_id]

        # ---------------------------------------
        # STEP 2: SESSION CREATION / UPDATE
        # ---------------------------------------
        if track_id in self.sessions:

            session = self.sessions[track_id]

            # update heartbeat
            session["last_seen"] = now

            return session

        # NEW SESSION OBJECT
        session = {
            "track_id": track_id,
            "visitor_id": visitor_id,

            "entry_emitted": False,
            "zone_emitted": set(),

            "entry_time": now,
            "last_seen": now,

            # will be used in Task 4.2 (EXIT)
            "exit_emitted": False,
            "active": True
        }

        self.sessions[track_id] = session
        return session

    # ---------------------------------------
    # HELPER: detect inactive sessions later
    # ---------------------------------------
    def get_inactive_sessions(self, timeout=5):

        now = time.time()
        inactive = []

        for track_id, session in self.sessions.items():

            if now - session["last_seen"] > timeout:
                inactive.append(session)

        return inactive
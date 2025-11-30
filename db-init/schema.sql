-- 1) BAZA WIEDZY
CREATE TABLE IF NOT EXISTS public.questions (
  question_id    bigserial PRIMARY KEY,
  question        text NOT NULL,
  correct_answer  text NOT NULL,
  context         text NOT NULL DEFAULT '',
  created_at      timestamptz NOT NULL DEFAULT now(),
  document_id     int4 not null
);

-- 2) HISTORIA ODPOWIEDZI (wiele prób)
CREATE TABLE IF NOT EXISTS public.user_answers (
  answer_id    bigserial PRIMARY KEY,
  question_id  int4,
  learner_key  uuid NOT NULL,
  user_answer  text NOT NULL,
  answered_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS user_answers_q_idx
  ON public.user_answers(question_id);

CREATE INDEX IF NOT EXISTS user_answers_learner_idx
  ON public.user_answers(learner_key);

CREATE INDEX IF NOT EXISTS user_answers_learner_q_time_idx
  ON public.user_answers(learner_key, question_id, answered_at DESC);

-- 3) PROGRES (1 rekord na learner_key + question)
CREATE TABLE IF NOT EXISTS public.user_progress (
  id              bigserial PRIMARY KEY,
  learner_key     uuid NOT NULL,
  question_id     int4,

  attempts_count  int NOT NULL DEFAULT 0 CHECK (attempts_count >= 0),
  best_score      int NOT NULL DEFAULT 0 CHECK (best_score BETWEEN 0 AND 100),
  last_score      int NOT NULL DEFAULT 0 CHECK (last_score BETWEEN 0 AND 100),
  gap_to_mastery  int NOT NULL DEFAULT 100 CHECK (gap_to_mastery BETWEEN 0 AND 100),
  status          text NOT NULL DEFAULT 'new'
                  CHECK (status IN ('new','learning','known','needs_review')),

  last_answer_at  timestamptz,
  updated_at      timestamptz NOT NULL DEFAULT now(),
  created_at      timestamptz NOT NULL DEFAULT now(),

  UNIQUE (learner_key, question_id)
);

CREATE INDEX IF NOT EXISTS user_progress_learner_idx
  ON public.user_progress(learner_key);

CREATE INDEX IF NOT EXISTS user_progress_question_idx
  ON public.user_progress(question_id);

CREATE INDEX IF NOT EXISTS user_progress_status_idx
  ON public.user_progress(status);

-- 4) CHAT SESSIONS
CREATE TABLE IF NOT EXISTS public.chat_sessions (
  id              uuid PRIMARY KEY,
  learner_key     uuid NOT NULL,
  title           text NOT NULL DEFAULT '',
  agent_code      text NOT NULL DEFAULT 'tutor',
  created_at      timestamptz NOT NULL DEFAULT now(),
  last_message_at timestamptz
);

CREATE INDEX IF NOT EXISTS chat_sessions_learner_idx
  ON public.chat_sessions(learner_key);

CREATE INDEX IF NOT EXISTS chat_sessions_last_msg_idx
  ON public.chat_sessions(last_message_at);

-- 5) CHAT MESSAGES
CREATE TABLE IF NOT EXISTS public.chat_messages (
  id            uuid PRIMARY KEY,
  session_id    uuid NOT NULL REFERENCES public.chat_sessions(id) ON DELETE CASCADE,
  role          text NOT NULL CHECK (role IN ('system','user','assistant','tool')),
  content       text NOT NULL,
  question_id   uuid REFERENCES public.questions(id) ON DELETE SET NULL,
  metadata_json jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chat_messages_session_time_idx
  ON public.chat_messages(session_id, created_at);

CREATE INDEX IF NOT EXISTS chat_messages_question_idx
  ON public.chat_messages(question_id);

-- 6) DOCUMENTS
CREATE TABLE IF NOT EXISTS public.documents (
  document_id    bigserial PRIMARY KEY,
  name           text NOT NULL,
  description    text NOT NULL DEFAULT '',
  content_type   text NOT NULL,
  data           bytea NOT NULL,
  text_data      text NOT NULL,
  rec_date       timestamptz NOT NULL DEFAULT now()
);


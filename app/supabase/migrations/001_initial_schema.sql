-- FoodIntel AI production database draft for Supabase Postgres.

create table if not exists companies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  industry text not null default 'Food industry sales',
  stripe_customer_id text,
  subscription_plan text default 'starter',
  created_at timestamptz default now()
);

create table if not exists seller_categories (
  id uuid primary key default gen_random_uuid(),
  company_id uuid references companies(id) on delete cascade,
  name text not null,
  product_focus text not null,
  target_customers text not null,
  created_at timestamptz default now()
);

create table if not exists products (
  id uuid primary key default gen_random_uuid(),
  company_id uuid references companies(id) on delete cascade,
  category_id uuid references seller_categories(id) on delete cascade,
  name text not null,
  use_case text not null,
  competitor_set text[],
  created_at timestamptz default now()
);

create table if not exists prospects (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  city text not null,
  area text not null,
  business_type text not null,
  rating numeric,
  outlet_count int default 1,
  created_at timestamptz default now()
);

create table if not exists meetings (
  id uuid primary key default gen_random_uuid(),
  company_id uuid references companies(id) on delete cascade,
  prospect_id uuid references prospects(id) on delete cascade,
  seller_category_id uuid references seller_categories(id),
  meeting_at timestamptz not null,
  meeting_goal text,
  stage text default 'pre_meeting',
  attendees jsonb default '[]'::jsonb,
  created_at timestamptz default now()
);

create table if not exists source_registry (
  id uuid primary key default gen_random_uuid(),
  prospect_id uuid references prospects(id) on delete cascade,
  source_type text not null,
  source_name text not null,
  source_url text,
  captured_at timestamptz default now(),
  confidence numeric not null default 0.8
);

create table if not exists raw_signals (
  id uuid primary key default gen_random_uuid(),
  prospect_id uuid references prospects(id) on delete cascade,
  source_id uuid references source_registry(id) on delete set null,
  source_type text not null,
  raw_text text not null,
  signal_date date,
  detected_topic text,
  sentiment text,
  relevance_score numeric default 0.75,
  created_at timestamptz default now()
);

create table if not exists insight_audit_logs (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references meetings(id) on delete cascade,
  prospect_id uuid references prospects(id) on delete cascade,
  source_ids uuid[],
  agent_name text not null,
  insight text not null,
  reasoning_summary text not null,
  confidence_score numeric not null,
  created_at timestamptz default now()
);

create table if not exists product_match_scores (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references meetings(id) on delete cascade,
  prospect_id uuid references prospects(id) on delete cascade,
  product_id uuid references products(id) on delete cascade,
  pain_point text not null,
  match_score int not null,
  reason text not null,
  recommended_pitch text not null,
  created_at timestamptz default now()
);

create table if not exists competitor_mentions (
  id uuid primary key default gen_random_uuid(),
  prospect_id uuid references prospects(id) on delete cascade,
  seller_category_id uuid references seller_categories(id),
  competitor_name text not null,
  competitor_type text not null,
  evidence text not null,
  source text not null,
  risk_level text not null,
  created_at timestamptz default now()
);

create table if not exists account_history (
  id uuid primary key default gen_random_uuid(),
  prospect_id uuid references prospects(id) on delete cascade,
  event_date date not null,
  event_type text not null,
  summary text not null,
  previous_value text,
  current_value text,
  impact text,
  created_at timestamptz default now()
);

create table if not exists brief_versions (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references meetings(id) on delete cascade,
  version int not null,
  generated_at timestamptz default now(),
  summary text not null,
  changes_from_previous text
);

create table if not exists followup_actions (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references meetings(id) on delete cascade,
  action_type text not null,
  status text not null default 'todo',
  due_date date,
  generated_by_ai boolean default true,
  created_at timestamptz default now()
);


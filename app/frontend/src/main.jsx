import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { api } from "./api";
import { captureEvent, initPostHog, stripeCheckout } from "./integrations";
import "./styles.css";

const pageOrder = [
  "Command Center",
  "Prospect Brief",
  "Opportunity Radar",
  "CRM Timeline",
  "Follow-up Studio",
  "AI Copilot",
  "AI Workflow",
  "Billing",
];

function Icon({ name, className = "" }) {
  const size = 18;
  const stroke = "currentColor";
  const strokeWidth = 2;
  const fill = "none";

  const icons = {
    "Command Center": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <rect x="3" y="3" width="7" height="9" rx="1" />
        <rect x="14" y="3" width="7" height="5" rx="1" />
        <rect x="14" y="12" width="7" height="9" rx="1" />
        <rect x="3" y="16" width="7" height="5" rx="1" />
      </svg>
    ),
    "Prospect Brief": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
        <polyline points="10 9 9 9 8 9" />
      </svg>
    ),
    "Opportunity Radar": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <circle cx="12" cy="12" r="10" />
        <circle cx="12" cy="12" r="6" />
        <circle cx="12" cy="12" r="2" />
        <line x1="12" y1="2" x2="12" y2="22" />
        <line x1="2" y1="12" x2="22" y2="12" />
      </svg>
    ),
    "CRM Timeline": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
    ),
    "Follow-up Studio": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
        <polyline points="22,6 12,13 2,6" />
      </svg>
    ),
    "AI Copilot": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707.707M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z" />
      </svg>
    ),
    "AI Workflow": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
      </svg>
    ),
    "Billing": (
      <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <rect x="2" y="5" width="20" height="14" rx="2" ry="2" />
        <line x1="2" y1="10" x2="22" y2="10" />
      </svg>
    ),
    "logout": (
      <svg width={16} height={16} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
        <polyline points="16 17 21 12 16 7" />
        <line x1="21" y1="12" x2="9" y2="12" />
      </svg>
    ),
    "user": (
      <svg width={16} height={16} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
    ),
    "area": (
      <svg width={16} height={16} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z" />
        <circle cx="12" cy="10" r="3" />
      </svg>
    ),
    "shield": (
      <svg width={16} height={16} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
      </svg>
    ),
    "download": (
      <svg width={16} height={16} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
      </svg>
    ),
    "check": (
      <svg width={14} height={14} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <polyline points="20 6 9 17 4 12" />
      </svg>
    ),
    "alert": (
      <svg width={16} height={16} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth={strokeWidth} className={className}>
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
    )
  };

  return icons[name] || null;
}

function App() {
  const [session, setSession] = useState(null);
  const [page, setPage] = useState("Command Center");
  const [area, setArea] = useState("");
  const [areas, setAreas] = useState([]);
  const [prospects, setProspects] = useState([]);
  const [activeProspect, setActiveProspect] = useState(null);
  const [command, setCommand] = useState(null);
  const [brief, setBrief] = useState(null);
  const [radar, setRadar] = useState(null);
  const [timeline, setTimeline] = useState(null);
  const [followup, setFollowup] = useState(null);
  const [workflow, setWorkflow] = useState(null);
  const [plans, setPlans] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    initPostHog();
  }, []);

  useEffect(() => {
    api.areas().then((data) => {
      setAreas(data.areas || []);
      setArea((data.areas || [])[0] || "");
    });
  }, []);

  useEffect(() => {
    if (!session?.category || !area) return;
    api.prospects(session.category, area).then((data) => {
      const nextProspects = data.prospects || [];
      setProspects(nextProspects);
      setActiveProspect((current) => {
        if (current && nextProspects.some((prospect) => prospect.id === current.id)) {
          return current;
        }
        return nextProspects[0] || null;
      });
    });
  }, [session, area]);

  useEffect(() => {
    if (!session?.category) return;
    api.commandCenter(session.category, area).then(setCommand);
    api.opportunityRadar(session.category).then(setRadar);
    api.workflow().then(setWorkflow);
    api.billingPlans().then(setPlans);
  }, [session, area]);

  useEffect(() => {
    if (!session?.category || !activeProspect?.id) return;
    api.brief(activeProspect.id, session.category).then(setBrief);
    api.crmTimeline(activeProspect.id, session.category).then(setTimeline);
    api.followup(activeProspect.id, session.category).then(setFollowup);
    api.track("prospect_selected", { prospect: activeProspect.name, category: session.category });
    captureEvent("prospect_selected", { prospect: activeProspect.name, category: session.category });
  }, [session, activeProspect]);

  const activeContext = useMemo(() => {
    if (!session) return null;
    return {
      seller: session.sellerCompany,
      category: session.category,
      prospect: activeProspect?.name || "No prospect selected",
      meeting: "Today 3:00 PM",
      productFocus: session.productFocus,
    };
  }, [session, activeProspect]);

  if (!session) return <LoginScreen onLogin={setSession} error={error} setError={setError} />;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark animate-shimmer">FI</div>
          <div>
            <strong>FoodIntel AI</strong>
            <span>Sales intelligence OS</span>
          </div>
        </div>
        <div className="login-card">
          <span className="eyebrow">Logged-in category</span>
          <strong>{session.category}</strong>
          <span>{session.sellerCompany}</span>
        </div>
        <label className="field">
          <span>Area</span>
          <div className="custom-select-wrapper">
            <Icon name="area" className="select-icon" />
            <select value={area} onChange={(event) => setArea(event.target.value)}>
              {areas.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </div>
        </label>
        <label className="field">
          <span>Active prospect</span>
          <div className="custom-select-wrapper">
            <Icon name="user" className="select-icon" />
            <select
              value={activeProspect?.id || ""}
              onChange={(event) => setActiveProspect(prospects.find((p) => p.id === event.target.value))}
            >
              {prospects.map((prospect) => (
                <option key={prospect.id} value={prospect.id}>
                  {prospect.name}
                </option>
              ))}
            </select>
          </div>
        </label>
        <nav>
          {pageOrder.map((item) => (
            <button className={page === item ? "active" : ""} key={item} onClick={() => setPage(item)}>
              <Icon name={item} className="nav-icon" />
              <span>{item}</span>
            </button>
          ))}
        </nav>
        <button className="logout" onClick={() => setSession(null)}>
          <Icon name="logout" className="nav-icon" />
          <span>Log out</span>
        </button>
      </aside>

      <main>
        <ContextBar context={activeContext} />
        <div className="page-container">
          {page === "Command Center" && (
            <CommandCenter command={command} onOpenBrief={(prospect) => { setActiveProspect(prospect); setPage("Prospect Brief"); }} />
          )}
          {page === "Prospect Brief" && <ProspectBrief brief={brief} />}
          {page === "Opportunity Radar" && <OpportunityRadar radar={radar} />}
          {page === "CRM Timeline" && <CRMTimeline timeline={timeline} />}
          {page === "Follow-up Studio" && <FollowUp followup={followup} />}
          {page === "AI Copilot" && <Copilot brief={brief} session={session} />}
          {page === "AI Workflow" && <Workflow workflow={workflow} />}
          {page === "Billing" && <Billing plans={plans} />}
        </div>
      </main>
    </div>
  );
}

function LoginScreen({ onLogin, error, setError }) {
  const [username, setUsername] = useState("packaging.rep@foodintel.ai");
  const [password, setPassword] = useState("packaging123");
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await api.login(username, password);
      onLogin(data.user);
      api.track("category_login_completed", { category: data.user.category });
      captureEvent("category_login_completed", { category: data.user.category });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-screen">
      <section className="login-panel">
        <div className="brand large animate-fade-in">
          <div className="brand-mark animate-shimmer">FI</div>
          <div>
            <strong>FoodIntel AI</strong>
            <span>AI Sales Intelligence Copilot</span>
          </div>
        </div>
        <h1>Login by sales category</h1>
        <p>
          The whole workspace becomes specific to what the salesperson sells: packaging,
          ingredients, beverages, hygiene, equipment, POS software or logistics.
        </p>
        <form onSubmit={submit}>
          <label className="field">
            <span>Username</span>
            <div className="input-with-icon">
              <Icon name="user" className="input-icon" />
              <input value={username} onChange={(event) => setUsername(event.target.value)} />
            </div>
          </label>
          <label className="field">
            <span>Password</span>
            <div className="input-with-icon">
              <Icon name="shield" className="input-icon" />
              <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            </div>
          </label>
          {error && <div className="error">{error}</div>}
          <button className="primary" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
        <div className="demo-logins">
          <strong>Demo logins</strong>
          <span>packaging.rep@foodintel.ai / packaging123</span>
          <span>ingredients.rep@foodintel.ai / ingredients123</span>
          <span>beverages.rep@foodintel.ai / beverages123</span>
        </div>
      </section>
    </div>
  );
}

function ContextBar({ context }) {
  if (!context) return null;
  const keyIcons = {
    seller: "user",
    category: "shield",
    prospect: "user",
    meeting: "CRM Timeline",
    productFocus: "AI Copilot"
  };
  return (
    <section className="context-bar">
      {Object.entries(context).map(([key, value]) => (
        <div key={key} className="context-item">
          <div className="context-item-header">
            <Icon name={keyIcons[key]} className="context-icon" />
            <span>{formatContextLabel(key)}</span>
          </div>
          <strong>{value}</strong>
        </div>
      ))}
    </section>
  );
}

function CommandCenter({ command, onOpenBrief }) {
  if (!command) return <Loading />;
  return (
    <Page title="Command Center" subtitle="Meeting priority only. Deep intelligence opens in Prospect Brief.">
      <div className="metric-grid">
        {Object.entries(command.metrics).map(([key, value]) => (
          <Metric key={key} label={labelize(key)} value={value} />
        ))}
      </div>
      <div className="two-col">
        <section className="panel">
          <h2>Today’s meetings</h2>
          <div className="table-list">
            {command.meetings.map((meeting) => (
              <button className="row-card" key={meeting.id} onClick={() => onOpenBrief(meeting)}>
                <div>
                  <strong>{meeting.name}</strong>
                  <span>{meeting.area} · {meeting.meetingTime}</span>
                </div>
                <div className="row-card-meta">
                  <Badge tone={meeting.priority === "High" ? "hot" : "warm"}>{meeting.priority}</Badge>
                  <strong className="opportunity-score">{meeting.opportunityScore}/100</strong>
                </div>
              </button>
            ))}
          </div>
        </section>
        <section className="panel">
          <h2>Smart alerts</h2>
          {command.alerts.map((alert) => (
            <InsightCard key={alert.title} title={alert.title} text={alert.detail} trust={alert} />
          ))}
        </section>
      </div>
    </Page>
  );
}

function ProspectBrief({ brief }) {
  if (!brief) return <Loading />;
  return (
    <Page title="Prospect Brief" subtitle="Deep company intelligence, product fit, explainability and pitch.">
      <div className="metric-grid">
        {Object.entries(brief.executiveSnapshot).map(([key, value]) => (
          <Metric key={key} label={labelize(key)} value={value} />
        ))}
      </div>
      <section className="panel">
        <h2>Account snapshot</h2>
        <div className="snapshot-grid">
          {Object.entries(brief.accountSnapshot || {}).map(([key, value]) => (
            <div className="snapshot-item" key={key}>
              <span>{labelize(key)}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      </section>
      <section className="panel">
        <h2>What changed since last meeting</h2>
        <div className="change-grid">
          {brief.whatChanged.map((item) => <ChangeCard item={item} key={item.title || item} />)}
        </div>
      </section>
      <div className="two-col">
        <section className="panel">
          <h2>AI-detected pain points</h2>
          {brief.painPoints.map((item) => (
            <InsightCard key={item.pain} title={item.pain} text={`${item.severity}: ${item.evidence}`} trust={item.trust} />
          ))}
        </section>
        <section className="panel">
          <h2>Product match intelligence</h2>
          {brief.productMatches.map((item) => (
            <div className="match-row" key={item.product}>
              <div>
                <strong>{item.product}</strong>
                <span>{item.reason}</span>
              </div>
              <Badge tone="good">{item.matchScore}</Badge>
            </div>
          ))}
        </section>
      </div>
      <div className="two-col">
        <section className="panel">
          <h2>Source registry</h2>
          {(brief.sourceRegistry || []).map((source) => (
            <div className="source-row" key={source.sourceType + source.sourceName}>
              <div>
                <strong>{source.sourceType}</strong>
                <span>{source.sourceName} · {source.capturedAt}</span>
                <small>{source.use}</small>
              </div>
              <Badge tone="good">{source.confidence}%</Badge>
            </div>
          ))}
        </section>
        <section className="panel">
          <h2>Raw signal feed</h2>
          {(brief.rawSignals || []).map((signal) => (
            <div className="source-row" key={signal.topic}>
              <div>
                <strong>{signal.topic}</strong>
                <span>{signal.signal}</span>
                <small>{signal.sentiment}</small>
              </div>
              <Badge tone="good">{signal.relevance}</Badge>
            </div>
          ))}
        </section>
      </div>
      <section className="panel">
        <h2>Competitor battlecard</h2>
        <div className="battlecard-grid">
          <TextBlock title="Likely competitors" items={brief.competitorBattlecard?.likelyCompetitors || []} />
          <TextBlock title="Comparison points" items={brief.competitorBattlecard?.comparisonPoints || []} />
          <TextBlock title="Where we win" text={brief.competitorBattlecard?.whereWeWin} />
          <TextBlock title="Verification note" text={brief.competitorBattlecard?.verificationNote} />
        </div>
      </section>
      <section className="panel">
        <h2>AI sales strategy</h2>
        <div className="strategy-grid">
          <TextBlock title="Opening" text={brief.strategy.opening} />
          <TextBlock title="Pitch" text={brief.strategy.pitch} />
          <TextBlock title="Questions" items={brief.strategy.questions} />
          <TextBlock title="Objection handling" items={brief.strategy.objections} />
        </div>
        <button className="primary download-btn" onClick={() => downloadPitch(brief)}>
          <Icon name="download" className="btn-icon" />
          <span>Download pitch Word doc</span>
        </button>
      </section>
      <section className="panel">
        <h2>Explainable AI insights</h2>
        {brief.insights.map((item) => (
          <InsightCard key={item.title} title={item.title} text={item.insight} trust={item.trust} />
        ))}
      </section>
    </Page>
  );
}

function OpportunityRadar({ radar }) {
  if (!radar) return <Loading />;
  return (
    <Page title="Opportunity Radar" subtitle="Cross-account category opportunities, not duplicate prospect intelligence.">
      <div className="two-col">
        <section className="panel">
          <h2>Sales opportunities</h2>
          {radar.opportunities.map((item) => (
            <div className="match-row" key={item.name}>
              <div>
                <strong>{item.name}</strong>
                <span>{item.accounts} matching accounts · {item.why}</span>
              </div>
              <Badge tone="good">{item.score}</Badge>
            </div>
          ))}
        </section>
        <section className="panel">
          <h2>Geographic opportunity clusters</h2>
          <div className="area-list">
            {radar.areaClusters.map(([area, count]) => (
              <div className="area-row" key={area}>
                <strong>{area}</strong>
                <span className="count-pill">{count} food businesses</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </Page>
  );
}

function CRMTimeline({ timeline }) {
  if (!timeline) return <Loading />;
  return (
    <Page title="CRM Timeline" subtitle="Relationship memory and what to carry into the next meeting.">
      <section className="timeline">
        {timeline.events.map((event) => (
          <div className="timeline-item" key={event.date + event.title}>
            <div className="timeline-node" />
            <div className="timeline-content">
              <span className="timeline-date">{event.date}</span>
              <strong>{event.title}</strong>
              <p>{event.note}</p>
              <div className="timeline-memory">
                <Icon name="AI Copilot" className="memory-icon" />
                <small>{event.aiMemory}</small>
              </div>
            </div>
          </div>
        ))}
      </section>
    </Page>
  );
}

function FollowUp({ followup }) {
  if (!followup) return <Loading />;
  return (
    <Page title="Follow-up Studio" subtitle="Post-meeting execution: email, CRM note and next actions.">
      <div className="two-col">
        <section className="panel">
          <h2>{followup.emailSubject}</h2>
          <pre>{followup.emailBody}</pre>
        </section>
        <section className="panel">
          <h2>CRM update</h2>
          <p className="crm-note">{followup.crmNote}</p>
          <div className="task-list">
            {followup.tasks.map((task) => (
              <div className="change-card task-card" key={task}>
                <Icon name="check" className="task-check-icon" />
                <span>{task}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </Page>
  );
}

function Copilot({ brief, session }) {
  const [question, setQuestion] = useState(`How should I pitch ${session.productFocus}?`);
  const [answer, setAnswer] = useState(() => buildCopilotFallback(brief, session, `How should I pitch ${session.productFocus}?`));
  const [loading, setLoading] = useState(false);
  const [copilotError, setCopilotError] = useState("");

  useEffect(() => {
    const defaultQuestion = `How should I pitch ${session.productFocus}?`;
    setQuestion(defaultQuestion);
    setAnswer(buildCopilotFallback(brief, session, defaultQuestion));
    setCopilotError("");
  }, [brief, session]);

  async function askCopilot() {
    if (!brief?.summary?.id) return;
    setLoading(true);
    setCopilotError("");
    try {
      const response = await api.copilot(question, brief.summary.id, session.category);
      setAnswer(response);
      api.track("copilot_question_asked", { question, category: session.category, prospect: brief?.summary?.name });
      captureEvent("copilot_question_asked", { question, category: session.category, prospect: brief?.summary?.name });
    } catch (error) {
      setCopilotError("Backend Copilot route is unavailable, showing local fallback reasoning.");
      setAnswer(buildCopilotFallback(brief, session, question));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Page title="AI Copilot" subtitle="Interactive reasoning only, not repeated dashboard content.">
      <section className="panel copilot">
        <label className="field">
          <span>Ask FoodIntel AI</span>
          <div className="copilot-input-wrapper">
            <input value={question} onChange={(event) => setQuestion(event.target.value)} />
            <button className="primary copilot-btn" onClick={askCopilot} disabled={loading}>
              {loading ? "Searching..." : "Ask"}
            </button>
          </div>
        </label>
        {copilotError && <div className="error inline-error">{copilotError}</div>}
        <div className="copilot-answer">
          <div className="copilot-answer-header">
            <Icon name="AI Copilot" className="copilot-glow-icon animate-pulse" />
            <span>Structured RAG Response</span>
          </div>
          <StructuredCopilotAnswer answer={answer} />
        </div>
      </section>
    </Page>
  );
}

function StructuredCopilotAnswer({ answer }) {
  if (!answer || typeof answer === "string") return <p>{answer || "Ask a question to generate a structured response."}</p>;
  return (
    <div className="structured-answer">
      <section className="rag-section answer-section">
        <h3>Answer</h3>
        <p>{answer.answer}</p>
      </section>

      <section className="rag-section">
        <h3>From Database</h3>
        <div className="rag-list">
          {(answer.fromDatabase || []).map((item) => (
            <article className="rag-card" key={item.title}>
              <strong>{item.title}</strong>
              <p>{item.detail}</p>
              <Badge tone="good">{item.relevance || item.confidence}%</Badge>
            </article>
          ))}
        </div>
      </section>

      <section className="rag-section">
        <h3>From Internet / Proxy Signals</h3>
        <div className="rag-list">
          {(answer.fromInternet || []).map((item) => (
            <article className="rag-card" key={item.title + item.source}>
              <strong>{item.title}</strong>
              <p>{item.detail}</p>
              <div className="trust-row">
                <span>{item.source}</span>
                <span>{item.confidence}% confidence</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="rag-section recommendation-section">
        <h3>Recommendation</h3>
        <p>{answer.recommendation}</p>
      </section>

      <section className="rag-section">
        <h3>Sources</h3>
        <div className="source-grid">
          {(answer.sources || []).map((source) => (
            <div className="source-chip" key={source.name + source.type}>
              <strong>{source.name}</strong>
              <span>{source.type}</span>
              <small>{source.timestamp} · {formatConfidence(source.confidence)}</small>
            </div>
          ))}
        </div>
      </section>

      <div className="copilot-workflow">
        {(answer.workflow || []).map((step, index) => (
          <span key={step}>{index + 1}. {step}</span>
        ))}
      </div>
      {answer.productionNote && <p className="production-note">{answer.productionNote}</p>}
    </div>
  );
}

function Workflow({ workflow }) {
  if (!workflow) return <Loading />;
  return (
    <Page title="AI Workflow" subtitle="Agentic Sales Intelligence Workflow with evidence and production API note.">
      <div className="two-col">
        <section className="panel">
          <h2>8 architecture layers</h2>
          {workflow.layers.map((layer, index) => <div className="flow-step" key={layer}><span className="step-num">{index + 1}</span> {layer}</div>)}
        </section>
        <section className="panel">
          <h2>7 AI agents</h2>
          {workflow.agents.map((agent, index) => <div className="flow-step" key={agent}><span className="step-num">{index + 1}</span> {agent}</div>)}
        </section>
      </div>
      <section className="panel">
        <h2>Evidence and audit store</h2>
        <div className="evidence-grid">
          {(workflow.evidenceStore || []).map((item) => (
            <div className="change-card" key={item}>{item}</div>
          ))}
        </div>
      </section>
      <section className="panel note">
        <Icon name="shield" className="note-icon" />
        <p>{workflow.productionNote}</p>
      </section>
    </Page>
  );
}

function Billing({ plans }) {
  if (!plans) return <Loading />;
  async function startCheckout(planName) {
    const result = await api.checkout(planName);
    if (result.checkoutUrl) {
      window.location.href = result.checkoutUrl;
      return;
    }
    alert(result.message || stripeCheckout(planName).message);
  }

  return (
    <Page title="Billing" subtitle="Stripe-ready SaaS packaging for production.">
      <section className="billing-note">
        Stripe is wired in demo mode. Live checkout activates when Stripe keys and price IDs are added.
      </section>
      <div className="plan-grid">
        {plans.plans.map((plan) => (
          <section className="panel plan" key={plan.name}>
            <div className="plan-header">
              <h2>{plan.name}</h2>
              <PlanPrice price={plan.price} />
            </div>
            <div className="plan-features">
              {plan.features.map((feature) => (
                <span key={feature} className="feature-item">
                  <Icon name="check" className="check-icon" />
                  <span>{feature}</span>
                </span>
              ))}
            </div>
            <button onClick={() => startCheckout(plan.name)} className="plan-btn">Start checkout</button>
          </section>
        ))}
      </div>
    </Page>
  );
}

function PlanPrice({ price }) {
  if (price === "Custom") {
    return <strong className="plan-price custom-price">Custom</strong>;
  }
  const [amount, cadence] = price.split("/");
  return (
    <div className="plan-price-group">
      <strong className="plan-price">{amount}</strong>
      <span className="plan-cadence">/{cadence}</span>
    </div>
  );
}

function Page({ title, subtitle, children }) {
  return (
    <div className="page animate-fade-in">
      <header>
        <span className="eyebrow">FoodIntel AI</span>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </header>
      {children}
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
      <div className="metric-glow" />
    </div>
  );
}

function Badge({ children, tone = "neutral" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

function ChangeCard({ item }) {
  if (typeof item === "string") return <div className="change-card">{item}</div>;
  return (
    <article className="change-card rich-change-card">
      <strong>{item.title}</strong>
      <p>{item.detail}</p>
      <div className="trust-row">
        <span>{item.source}</span>
        <span>{item.confidence}% confidence</span>
      </div>
    </article>
  );
}

function InsightCard({ title, text, trust }) {
  return (
    <article className="insight-card">
      <div className="insight-header">
        <Icon name="alert" className="insight-header-icon" />
        <strong>{title}</strong>
      </div>
      <p>{text}</p>
      <div className="trust-row">
        <span>{trust.source}</span>
        <span>{trust.timestamp || "Live demo"}</span>
        <span>{trust.confidence}% confidence</span>
      </div>
      {trust.whyThisMatters && <small className="why-matters">{trust.whyThisMatters}</small>}
    </article>
  );
}

function TextBlock({ title, text, items }) {
  return (
    <div className="text-block">
      <strong>{title}</strong>
      {items ? (
        <ul className="question-list">
          {items.map((item) => <li key={item}>{item}</li>)}
        </ul>
      ) : (
        <p>{text}</p>
      )}
    </div>
  );
}

function Loading() {
  return (
    <div className="loading">
      <div className="loading-spinner" />
      <span>Loading FoodIntel intelligence...</span>
    </div>
  );
}

function labelize(key) {
  return key.replace(/([A-Z])/g, " $1").replace(/^./, (char) => char.toUpperCase());
}

function formatContextLabel(key) {
  const labels = {
    seller: "Seller",
    category: "Category",
    prospect: "Prospect",
    meeting: "Meeting",
    productFocus: "Product Focus",
  };
  return labels[key] || labelize(key);
}

function formatConfidence(value) {
  return typeof value === "number" ? `${value}% confidence` : value;
}

function buildCopilotFallback(brief, session, question) {
  if (!brief) return "Select a prospect to generate AI reasoning.";
  const normalized = question.toLowerCase();
  const prospect = brief.summary.name;
  const productFocus = session.productFocus;
  const topMatch = brief.productMatches?.[0]?.product || productFocus;

  if (normalized.includes("objection") || normalized.includes("price")) {
    return `For ${prospect}, expect price and current-supplier objections. Anchor the discussion on ${productFocus}, propose a small pilot with ${topMatch}, and compare total issue reduction instead of only unit price.`;
  }
  if (normalized.includes("question") || normalized.includes("ask")) {
    return `Ask three things: who the current ${session.category} supplier is, what issue would justify switching, and whether quality, reliability, replacement policy or price matters most.`;
  }
  if (normalized.includes("competitor")) {
    return `Use competitor discovery carefully: ask if they use known category players or local suppliers, then compare on reliability, replacement policy, SKU fit and service response.`;
  }
  if (normalized.includes("follow")) {
    return `Send a short follow-up with one pilot proposal, one decision-maker confirmation, and one sample-review date. Keep it tied to ${productFocus}, not a broad catalog.`;
  }
  return `For ${prospect}, position ${productFocus} through a small pilot. Lead with ${topMatch}, ask about the current supplier, then handle risk by comparing operational impact, switching effort and replacement terms.`;
}

function downloadPitch(brief) {
  const html = `
    <html>
      <head><meta charset="utf-8"><title>FoodIntel AI Pitch</title></head>
      <body>
        <h1>FoodIntel AI Pitch - ${escapeHtml(brief.summary.name)}</h1>
        <p><strong>Seller:</strong> ${escapeHtml(brief.context.seller)}</p>
        <p><strong>Category:</strong> ${escapeHtml(brief.context.category)}</p>
        <p><strong>Product Focus:</strong> ${escapeHtml(brief.context.productFocus)}</p>
        <h2>Opening</h2>
        <p>${escapeHtml(brief.strategy.opening)}</p>
        <h2>Pitch</h2>
        <p>${escapeHtml(brief.strategy.pitch)}</p>
        <h2>Questions</h2>
        <ul>${brief.strategy.questions.map((q) => `<li>${escapeHtml(q)}</li>`).join("")}</ul>
        <h2>Objection Handling</h2>
        <ul>${brief.strategy.objections.map((o) => `<li>${escapeHtml(o)}</li>`).join("")}</ul>
      </body>
    </html>
  `;
  const blob = new Blob([html], { type: "application/msword" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${brief.summary.name.replaceAll(" ", "-")}-pitch.doc`;
  link.click();
  URL.revokeObjectURL(url);
  api.track("pitch_downloaded", { prospect: brief.summary.name, category: brief.context.category });
  captureEvent("pitch_downloaded", { prospect: brief.summary.name, category: brief.context.category });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

createRoot(document.getElementById("root")).render(<App />);

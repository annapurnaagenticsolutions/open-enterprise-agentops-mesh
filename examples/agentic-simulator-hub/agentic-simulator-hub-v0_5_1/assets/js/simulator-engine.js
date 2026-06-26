(function () {
  const data = window.AAS_SIMULATOR_DATA;

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>'"]/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      '"': "&quot;"
    }[char]));
  }

  function clean(value, fallback) {
    const str = String(value ?? "").trim();
    return str || fallback;
  }

  function listFromText(value, fallbackItems) {
    const items = String(value ?? "")
      .split(/\n|,|;/)
      .map((item) => item.trim())
      .filter(Boolean);
    return items.length ? items : fallbackItems;
  }

  function scoreLabel(score) {
    if (score >= 85) return "Strong";
    if (score >= 70) return "Good";
    if (score >= 55) return "Needs review";
    return "Early draft";
  }

  function languageNote(language, domain) {
    const notes = {
      Business: {
        English: "Keep the public page clear, credible, and easy to act on.",
        Hindi: "संदेश सरल, भरोसेमंद और स्पष्ट रखें।",
        Hinglish: "Message simple, clear aur trust-focused rakhein.",
        Odia: "ସନ୍ଦେଶକୁ ସରଳ, ସ୍ପଷ୍ଟ ଏବଂ ଭରସାଯୋଗ୍ୟ ରଖନ୍ତୁ।"
      },
      Education: {
        English: "Use learner-level language and verify conceptual accuracy.",
        Hindi: "विद्यार्थी के स्तर के अनुसार सरल भाषा और सही अवधारणा रखें।",
        Hinglish: "Learner ke level ke hisaab se simple explanation dein.",
        Odia: "ଶିକ୍ଷାର୍ଥୀଙ୍କ ସ୍ତର ଅନୁଯାୟୀ ସରଳ ଭାଷା ବ୍ୟବହାର କରନ୍ତୁ।"
      },
      Safety: {
        English: "Do not ask for OTP, PIN, password, or account details.",
        Hindi: "OTP, PIN, password या account details कभी न माँगें।",
        Hinglish: "OTP, PIN, password ya account details kabhi mat maangiye.",
        Odia: "OTP, PIN, password କିମ୍ବା account details କେବେ ମାଗନ୍ତୁ ନାହିଁ।"
      },
      Workflow: {
        English: "Keep roles bounded and put human approval before external action.",
        Hindi: "हर agent role सीमित रखें और external action से पहले human approval रखें।",
        Hinglish: "Agent roles bounded rakhein aur external action se pehle human approval rakhein.",
        Odia: "Agent role ସୀମିତ ରଖନ୍ତୁ ଏବଂ external action ପୂର୍ବରୁ human approval ରଖନ୍ତୁ।"
      },
      Strategy: {
        English: "Validate demand before building production features.",
        Hindi: "Production build से पहले real demand validate करें।",
        Hinglish: "Production build se pehle real demand validate karna zaroori hai.",
        Odia: "Production build ପୂର୍ବରୁ real demand validate କରନ୍ତୁ।"
      }
    };
    return (notes[domain] && notes[domain][language]) || notes[domain]?.English || "Review before use.";
  }

  function baseResult(simulator, title, summary, workflow, scorecard, sections, pitchNote) {
    return {
      product: data.product,
      version: data.version,
      simulatorId: simulator.id,
      simulatorTitle: simulator.title,
      category: simulator.category,
      isolationRule: simulator.isolationRule,
      title,
      summary,
      workflow,
      scorecard,
      sections,
      pitchNote
    };
  }

  function generateBusiness(values, simulator) {
    const scenarioName = clean(values.businessScenario, "Tuition Teacher");
    const scenario = data.businessScenarios[scenarioName] || data.businessScenarios["Tuition Teacher"];
    const businessName = clean(values.businessName, scenario.defaultName);
    const location = clean(values.businessLocation, scenario.defaultLocation);
    const services = listFromText(values.businessServices, scenario.services);
    const language = clean(values.businessLanguage, "English");
    const tone = clean(values.businessTone, "Trust-focused");

    return baseResult(
      simulator,
      `${businessName} — ${scenarioName} landing-page draft`,
      `A ${tone.toLowerCase()} local business page for ${scenario.audience} in ${location}.`,
      [
        "Read only the selected business scenario and owner-provided service list.",
        "Generate business-page copy: hero, about, services, proof, CTA, and publishing checklist.",
        "Apply local-language sharing guidance without translating into unsupported claims.",
        "Block false guarantees, fake reviews, unverifiable awards, and unclear promises.",
        "Return copy that the business owner must review before publishing."
      ],
      { "Scenario fit": 91, "Copy clarity": 88, "Safety readiness": 86, "Owner-review readiness": 84 },
      [
        { heading: "Hero section", html: `<p><strong>${escapeHtml(scenario.hero)}</strong></p><p>${escapeHtml(location)} · ${escapeHtml(tone)} communication</p>` },
        { heading: "About section", html: `<p>${escapeHtml(businessName)} ${escapeHtml(scenario.about)}.</p>` },
        { heading: "Key services", html: `<ul>${services.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` },
        { heading: "Trust indicators", html: `<ul>${scenario.proof.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` },
        { heading: `${escapeHtml(language)} sharing note`, html: `<p>${escapeHtml(languageNote(language, "Business"))}</p><p><strong>CTA:</strong> ${escapeHtml(scenario.cta)}</p>` },
        { heading: "Publishing boundary", html: `<ul><li>${escapeHtml(scenario.caution)}</li><li>Use only real contact details, actual service availability, and owner-approved pricing.</li><li>Do not create fake customer testimonials or ratings.</li></ul>` }
      ],
      "Client value: converts local-business details into page-ready communication while keeping claims reviewable and credible."
    );
  }

  function generateEducation(values, simulator) {
    const topicName = clean(values.eduTopic, "Photosynthesis");
    const topic = data.educationTopics[topicName] || data.educationTopics.Photosynthesis;
    const level = clean(values.eduClassLevel, topic.defaultClass);
    const style = clean(values.eduStyle, "Simple");
    const language = clean(values.eduLanguage, "English");

    return baseResult(
      simulator,
      `${topicName} — learner explanation`,
      `A ${style.toLowerCase()} explanation for ${level}, with analogy, misconception check, and practice question.`,
      [
        "Read only the selected learning topic and learner level.",
        "Explain the concept in age-appropriate language.",
        "Add one analogy, one misconception warning, and one practice question.",
        "Avoid unsupported curriculum claims and unsafe experiments.",
        "Return a concise revision card for learner review."
      ],
      { "Concept clarity": 90, "Learner fit": 86, "Misconception coverage": 88, "Safety readiness": 84 },
      [
        { heading: "Simple explanation", html: `<p>${escapeHtml(topic.simple)}</p>` },
        { heading: "Analogy", html: `<p>${escapeHtml(topic.analogy)}</p>` },
        { heading: "Common misconception", html: `<p>${escapeHtml(topic.misconception)}</p>` },
        { heading: "Practice check", html: `<p><strong>Question:</strong> ${escapeHtml(topic.question)}</p><p><strong>Expected answer:</strong> ${escapeHtml(topic.answer)}</p>` },
        { heading: `${escapeHtml(language)} learner note`, html: `<p>${escapeHtml(languageNote(language, "Education"))}</p>` },
        { heading: "Teaching boundary", html: `<ul><li>${escapeHtml(topic.safeNote)}</li><li>This is a learning explanation, not a certified curriculum replacement.</li><li>Teacher or parent review is recommended before classroom use.</li></ul>` }
      ],
      "Client value: demonstrates learner-friendly explanation support with misconception checks and teacher/parent review boundaries."
    );
  }

  function generateSafety(values, simulator) {
    const scenarioName = clean(values.safetyScenario, "OTP Sharing Phone Call");
    const scenario = data.safetyScenarios[scenarioName] || data.safetyScenarios["OTP Sharing Phone Call"];
    const audience = clean(values.safetyAudience, "General user");
    const action = clean(values.safetyAction, "The user is unsure what to do next.");
    const language = clean(values.safetyLanguage, "English");

    return baseResult(
      simulator,
      `${scenarioName} — safety coaching result`,
      `${audience} scenario classified as ${scenario.level} risk with safer next action guidance.`,
      [
        "Read only the selected digital-safety scenario and user action.",
        "Classify risk without asking for sensitive account details.",
        "Explain warning signs and safer next action.",
        "Provide a short response the user can say or send.",
        "Avoid panic, legal accusation, or security-bypass guidance."
      ],
      { "Risk clarity": 92, "Action safety": 94, "Audience fit": 84, "Trainer readiness": 88 },
      [
        { heading: "Risk classification", html: `<p><strong>${escapeHtml(scenario.level)} risk.</strong> ${escapeHtml(scenario.reason)}</p>` },
        { heading: "User action reviewed", html: `<p>${escapeHtml(action)}</p>` },
        { heading: "Safer action", html: `<p>${escapeHtml(scenario.saferAction)}</p>` },
        { heading: "Warning signs", html: `<ul>${scenario.warningSigns.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` },
        { heading: "Do not do", html: `<ul>${scenario.dontDo.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` },
        { heading: `${escapeHtml(language)} safety note`, html: `<p>${escapeHtml(languageNote(language, "Safety"))}</p><p><strong>Safe response:</strong> ${escapeHtml(scenario.message)}</p>` }
      ],
      "Client value: supports digital-confidence training by guiding safer actions without collecting sensitive account information."
    );
  }

  function generateWorkflow(values, simulator) {
    const useCase = clean(values.workflowUseCase, "Agent that drafts replies to customer enquiries");
    const domain = clean(values.workflowDomain, "Business");
    const risk = clean(values.workflowRiskLevel, "Medium");
    const output = clean(values.workflowOutputType, "Implementation blueprint");
    const language = clean(values.workflowLanguage, "English");
    const reviewStrictness = risk === "High" ? "mandatory human approval before every external action" : risk === "Medium" ? "human review before sending or publishing" : "sample review and escalation for unclear cases";

    return baseResult(
      simulator,
      `${domain} workflow — ${output}`,
      `A bounded multi-agent workflow blueprint for: ${useCase}.`,
      [
        "Clarify use case, domain, risk level, and expected output.",
        "Assign bounded roles: Planner, Worker, Reviewer, and Human Approver.",
        "Define inputs, tools, outputs, handoff conditions, and failure states.",
        "Add approval gates based on risk level.",
        "Return a blueprint only; clearly separate preview output from production deployment."
      ],
      { "Role clarity": 90, "Governance design": risk === "High" ? 92 : 86, "Implementation readiness": 76, "Pilot suitability": 82 },
      [
        { heading: "Agent roles", html: `<ol><li><strong>Planner:</strong> Breaks the use case into steps and identifies missing information.</li><li><strong>Worker:</strong> Drafts the requested output using approved inputs.</li><li><strong>Reviewer:</strong> checks factuality, tone, safety, and completeness.</li><li><strong>Human Approver:</strong> approves, edits, or rejects external-facing output.</li></ol>` },
        { heading: "Approval rule", html: `<p>${escapeHtml(reviewStrictness)}.</p>` },
        { heading: "Tool boundary", html: `<ul><li>Use only approved data sources.</li><li>Log generated outputs and review decisions.</li><li>Escalate ambiguous or sensitive cases.</li></ul>` },
        { heading: `${escapeHtml(language)} architecture note`, html: `<p>${escapeHtml(languageNote(language, "Workflow"))}</p>` },
        { heading: "Pilot path", html: `<ol><li>Test 10 realistic workflow examples.</li><li>Review all outputs manually.</li><li>Define failure patterns and escalation rules.</li><li>Only then consider backend/LLM integration.</li></ol>` }
      ],
      "Client value: shows how agent roles, review checkpoints, and approval gates can make automation understandable and governable."
    );
  }

  function generateOpportunity(values, simulator) {
    const idea = clean(values.opportunityIdea, "Agentic solution idea");
    const user = clean(values.opportunityUser, "Target users");
    const urgency = clean(values.opportunityUrgency, "Medium");
    const sensitivity = clean(values.opportunitySensitivity, "Medium");
    const monetization = clean(values.opportunityMonetization, "Service package + setup fee");
    const language = clean(values.opportunityLanguage, "English");
    const proceedScore = (urgency === "High" ? 35 : urgency === "Medium" ? 25 : 15) + (sensitivity === "Low" ? 30 : sensitivity === "Medium" ? 20 : 8) + 30;
    const recommendation = proceedScore >= 82 ? "Prototype now" : proceedScore >= 65 ? "Prototype with strict scope" : proceedScore >= 50 ? "Validate before build" : "Defer or re-scope";

    return baseResult(
      simulator,
      `Opportunity evaluation — ${recommendation}`,
      `Assessment for ${user}: ${idea}.`,
      [
        "Clarify target user, pain intensity, monetization, and sensitivity.",
        "Check whether the idea needs agentic workflow or only a simpler static tool.",
        "Define exclusions before development starts.",
        "Recommend prototype, validation, deferral, or re-scope.",
        "Return next evidence needed for decision-making."
      ],
      { "Problem urgency": urgency === "High" ? 90 : urgency === "Medium" ? 72 : 48, "Risk manageability": sensitivity === "Low" ? 88 : sensitivity === "Medium" ? 70 : 42, "Monetization clarity": monetization.length > 10 ? 78 : 55, "Prototype fit": proceedScore },
      [
        { heading: "Recommendation", html: `<p><strong>${escapeHtml(recommendation)}</strong></p><p>This idea should move forward only with a narrow pilot scope and clear evidence targets.</p>` },
        { heading: "User and value", html: `<p><strong>Target user:</strong> ${escapeHtml(user)}</p><p><strong>Idea:</strong> ${escapeHtml(idea)}</p>` },
        { heading: "Commercial note", html: `<p>${escapeHtml(monetization)}</p>` },
        { heading: "Scope boundary", html: `<ul><li>Do not collect unnecessary personal or sensitive data.</li><li>Start with a controlled workflow preview before backend integration.</li><li>Use human review for all external-facing recommendations.</li></ul>` },
        { heading: `${escapeHtml(language)} validation note`, html: `<p>${escapeHtml(languageNote(language, "Strategy"))}</p>` },
        { heading: "Next validation", html: `<ol><li>Interview 5 target users.</li><li>Run 10 sample scenarios.</li><li>Measure time saved and output acceptance.</li><li>Decide build/defer after evidence review.</li></ol>` }
      ],
      "Client value: helps decide whether to prototype, validate, re-scope, or defer before investing in development."
    );
  }

  function generate(simulator, values) {
    if (!simulator || !simulator.id) throw new Error("Missing simulator");
    switch (simulator.id) {
      case "business-page-generator": return generateBusiness(values, simulator);
      case "education-concept-tutor": return generateEducation(values, simulator);
      case "digital-safety-coach": return generateSafety(values, simulator);
      case "multi-agent-workflow-designer": return generateWorkflow(values, simulator);
      case "solution-opportunity-evaluator": return generateOpportunity(values, simulator);
      default: throw new Error(`Unknown simulator id: ${simulator.id}`);
    }
  }

  window.AAS_SimulatorEngine = {
    escapeHtml,
    clean,
    generate,
    scoreLabel
  };
})();

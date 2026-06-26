(function () {
  const VERSION = "0.5.1";
  const PRODUCT = "Annapurna Agentic Solutions — Agentic Solutions Studio";
  const languages = ["English", "Hindi", "Hinglish", "Odia"];

  window.AAS_SIMULATOR_DATA = {
    version: VERSION,
    product: PRODUCT,
    categories: ["All", "Business", "Education", "Digital Safety", "Agentic Automation", "Strategy"],
    businessScenarios: {
      "Tuition Teacher": {
        defaultName: "Bright Steps Tuition",
        defaultLocation: "Whitefield, Bengaluru",
        audience: "school students and parents",
        hero: "Clear concept support for school learners",
        about: "helps students understand difficult topics through simple explanations, regular practice, and parent-friendly progress updates",
        services: ["Class 6-10 Maths", "Science basics", "Weekly revision tests", "Parent progress updates"],
        proof: ["Structured weekly classes", "Concept-first teaching", "Practice and revision support"],
        caution: "Avoid guaranteed marks, rank promises, or unverifiable success claims.",
        cta: "Message us to discuss class timing, subjects, and student learning needs."
      },
      "Small Clinic": {
        defaultName: "Care First Clinic",
        defaultLocation: "Bhubaneswar",
        audience: "local families and patients",
        hero: "Simple clinic information for local patients",
        about: "shares clinic timing, basic services, appointment guidance, and patient communication in a clear and responsible way",
        services: ["General consultation", "Basic health check-up", "Follow-up appointment guidance", "Clinic timing information"],
        proof: ["Clear appointment process", "Transparent service list", "Responsible health communication"],
        caution: "Do not claim cures, emergency capability, specialist status, or outcomes unless verified by the clinic owner.",
        cta: "Contact the clinic for timing, appointment availability, and service confirmation."
      },
      "Local Restaurant": {
        defaultName: "Annapurna Family Kitchen",
        defaultLocation: "Koramangala, Bengaluru",
        audience: "nearby families, office workers, and regular customers",
        hero: "Fresh local food with simple ordering information",
        about: "presents menu highlights, ordering channels, opening hours, and customer-friendly food information without exaggerated claims",
        services: ["Breakfast and meals", "Family dine-in", "Takeaway orders", "Small party food orders"],
        proof: ["Menu clarity", "Ordering channel", "Opening-hour visibility"],
        caution: "Avoid unverified health, ingredient, certification, hygiene, or award claims.",
        cta: "Call or message us for today’s menu, takeaway orders, and timing."
      },
      "Home Service Provider": {
        defaultName: "QuickFix Home Services",
        defaultLocation: "Marathahalli, Bengaluru",
        audience: "households needing reliable local service",
        hero: "Reliable local service with clear booking steps",
        about: "helps residents understand available services, service areas, booking process, and expected owner confirmation before visit",
        services: ["Electrical repair", "Plumbing support", "Appliance inspection", "Scheduled home visits"],
        proof: ["Service-area clarity", "Transparent booking path", "Owner-confirmed availability"],
        caution: "Avoid fake reviews, guaranteed repair claims, or unclear pricing promises.",
        cta: "Share your service need and location to check availability."
      }
    },
    educationTopics: {
      "Photosynthesis": {
        defaultClass: "Class 6-8",
        simple: "Plants use sunlight, water, and carbon dioxide to make glucose as food. Oxygen is released as a useful by-product.",
        analogy: "Think of a leaf as a small kitchen. Sunlight gives energy, water and carbon dioxide are ingredients, and glucose is the food prepared inside.",
        misconception: "Plants do not eat soil as food. Soil gives minerals and support, but the plant mainly makes food through photosynthesis.",
        question: "What three things does a plant mainly need for photosynthesis?",
        answer: "Sunlight, water, and carbon dioxide.",
        safeNote: "Keep the explanation conceptual. Avoid unsafe experiments involving chemicals or fire."
      },
      "Fractions": {
        defaultClass: "Class 3-5",
        simple: "A fraction shows part of a whole. The numerator tells how many parts we have; the denominator tells how many equal parts the whole is divided into.",
        analogy: "If a roti is cut into four equal pieces and you take one piece, you have one-fourth of the roti.",
        misconception: "A bigger denominator does not always mean a bigger value. One-eighth is smaller than one-fourth when the whole is the same size.",
        question: "Which is bigger: 1/3 or 1/6?",
        answer: "1/3 is bigger because the whole is divided into fewer equal parts.",
        safeNote: "Use age-appropriate examples and avoid overloading the learner with notation."
      },
      "Electricity Basics": {
        defaultClass: "Class 6-8",
        simple: "Electricity is the movement of electric charge through a path called a circuit. A closed circuit lets current flow; an open circuit stops it.",
        analogy: "Imagine water moving through a pipe. If the pipe is blocked, water cannot flow. A broken circuit works similarly.",
        misconception: "A battery does not create unlimited electricity. It provides stored energy that pushes charge through a circuit.",
        question: "What happens when a switch opens a circuit?",
        answer: "Current stops flowing.",
        safeNote: "Use only low-risk classroom diagrams. Do not instruct children to handle mains electricity."
      },
      "Atoms and Molecules": {
        defaultClass: "Class 6-8",
        simple: "Atoms are tiny building blocks of matter. Molecules form when two or more atoms join together.",
        analogy: "Letters join to make words. Similarly, atoms join to make molecules.",
        misconception: "Atoms are not usually visible through a school microscope; they are far smaller than cells.",
        question: "What is formed when two or more atoms join together?",
        answer: "A molecule.",
        safeNote: "Avoid advanced atomic models unless the learner level is ready."
      }
    },
    safetyScenarios: {
      "Unknown UPI Payment Request": {
        level: "High",
        reason: "Unexpected payment requests can be fraud attempts, especially when urgency or emotional pressure is used.",
        saferAction: "Do not approve the request. Verify the person through a trusted channel before taking any action.",
        warningSigns: ["Unknown requester", "Urgent payment pressure", "Unclear reason", "Request to act without checking"],
        dontDo: ["Do not enter UPI PIN to receive money", "Do not approve unknown collect requests", "Do not share screenshots containing account information"],
        message: "I will verify this request directly before approving anything."
      },
      "OTP Sharing Phone Call": {
        level: "Critical",
        reason: "OTP can authorize account access or transactions. Genuine banks and services do not need your OTP over a call.",
        saferAction: "Disconnect the call, do not share OTP, and contact the official support number if needed.",
        warningSigns: ["Asking for OTP", "Threatening account closure", "Claiming urgent verification", "Requesting screen sharing"],
        dontDo: ["Do not share OTP", "Do not install remote-access apps", "Do not follow caller-provided links"],
        message: "I do not share OTPs or banking details on calls. I will contact official support separately."
      },
      "Fake Job Message": {
        level: "High",
        reason: "Fraudulent job messages often ask for fees, documents, or bank details before verification.",
        saferAction: "Check the company domain, recruiter identity, role details, and fee demands before responding.",
        warningSigns: ["Registration fee", "Too-good salary", "No official email", "Immediate document demand"],
        dontDo: ["Do not pay for job confirmation", "Do not send sensitive documents on chat", "Do not trust only logo screenshots"],
        message: "Please send the official company page, role description, and recruiter email for verification."
      },
      "Suspicious App Permissions": {
        level: "Medium",
        reason: "Apps asking for unrelated permissions may expose contacts, photos, location, or messages unnecessarily.",
        saferAction: "Review permissions, deny unrelated access, and use trusted app sources.",
        warningSigns: ["Unrelated SMS access", "Contact access without need", "Unknown developer", "Poor reviews"],
        dontDo: ["Do not grant all permissions blindly", "Do not install from unknown links", "Do not ignore repeated warning screens"],
        message: "I will install only from a trusted source and allow only permissions needed for the app function."
      }
    },
    simulators: [
      {
        id: "business-page-generator",
        title: "Local Language Business Page Generator",
        category: "Business",
        icon: "🏪",
        description: "Create clear local-language landing-page copy for a selected business category.",
        tags: ["Business", "Local language", "Landing page"],
        buyer: "MSMEs, local services, family-run businesses",
        maturity: "Prototype-ready",
        pitchValue: "Shows a concrete commercial output for local-business visibility.",
        isolationRule: "Only business-page content, service copy, and publishing checks are generated.",
        fields: [
          { id: "businessScenario", label: "Business scenario", type: "select", optionsFrom: "businessScenarios" },
          { id: "businessName", label: "Business name", type: "text" },
          { id: "businessLocation", label: "Location", type: "text" },
          { id: "businessServices", label: "Key services", type: "textarea", rows: 5 },
          { id: "businessLanguage", label: "Output language", type: "select", options: languages },
          { id: "businessTone", label: "Tone", type: "select", options: ["Trust-focused", "Friendly", "Professional", "Simple local"] }
        ]
      },
      {
        id: "education-concept-tutor",
        title: "Education Concept Tutor",
        category: "Education",
        icon: "📘",
        description: "Explain one learning concept with misconception check, analogy, and practice question.",
        tags: ["Learning", "Concept clarity", "Misconception check"],
        buyer: "Schools, tutors, education demos, learning labs",
        maturity: "Demo-ready",
        pitchValue: "Connects the portfolio to Jigyasu, WonderHub, and STEM learning assets.",
        isolationRule: "Only education explanation, learner support, and practice output are generated.",
        fields: [
          { id: "eduTopic", label: "Concept topic", type: "select", optionsFrom: "educationTopics" },
          { id: "eduClassLevel", label: "Learner level", type: "select", options: ["Class 1-2", "Class 3-5", "Class 6-8", "Class 9-10"] },
          { id: "eduStyle", label: "Teaching style", type: "select", options: ["Simple", "Story-based", "Example-based", "Quiz-first"] },
          { id: "eduLanguage", label: "Output language", type: "select", options: languages }
        ]
      },
      {
        id: "digital-safety-coach",
        title: "Digital Safety Scenario Coach",
        category: "Digital Safety",
        icon: "🛡️",
        description: "Classify digital-risk scenarios and generate safer next actions.",
        tags: ["Trust", "Safety", "Digital confidence"],
        buyer: "NGOs, schools, trainers, senior groups, public-awareness programs",
        maturity: "Pilot-kit ready",
        pitchValue: "Shows responsible social-impact use cases with clear boundaries.",
        isolationRule: "Only digital-safety coaching and safe action guidance are generated.",
        fields: [
          { id: "safetyScenario", label: "Safety scenario", type: "select", optionsFrom: "safetyScenarios" },
          { id: "safetyAudience", label: "Audience", type: "select", options: ["Student", "Parent", "Senior citizen", "Small business owner", "General user"] },
          { id: "safetyAction", label: "What the user is about to do", type: "textarea", rows: 4, placeholder: "Example: I am about to approve a payment request because the caller says it is urgent." },
          { id: "safetyLanguage", label: "Output language", type: "select", options: languages }
        ]
      },
      {
        id: "multi-agent-workflow-designer",
        title: "Multi-Agent Workflow Designer",
        category: "Agentic Automation",
        icon: "🧩",
        description: "Design a safe Planner → Worker → Reviewer → Human Approval workflow blueprint.",
        tags: ["Agent roles", "Workflow", "Governance"],
        buyer: "Teams exploring practical agentic automation",
        maturity: "Architecture-demo ready",
        pitchValue: "Shows that Annapurna can design governed workflows, not only prompt demos.",
        isolationRule: "Only agent-role workflow blueprint and approval design are generated.",
        fields: [
          { id: "workflowUseCase", label: "Solution use case", type: "textarea", rows: 4, placeholder: "Example: Agent that drafts replies to school enquiry messages" },
          { id: "workflowDomain", label: "Domain", type: "select", options: ["Business", "Education", "Digital Safety", "MSME/Startup", "Internal Operations"] },
          { id: "workflowRiskLevel", label: "Risk level", type: "select", options: ["Low", "Medium", "High"] },
          { id: "workflowOutputType", label: "Expected output", type: "select", options: ["Implementation blueprint", "Demo workflow", "Prompt pack", "Human review process"] },
          { id: "workflowLanguage", label: "Output language", type: "select", options: languages }
        ]
      },
      {
        id: "solution-opportunity-evaluator",
        title: "Agentic Solution Opportunity Evaluator",
        category: "Strategy",
        icon: "🧭",
        description: "Evaluate whether an agentic solution idea should be prototyped, validated, deferred, or re-scoped.",
        tags: ["Product strategy", "Prioritization", "Pilot scope"],
        buyer: "Founders, product owners, portfolio decision-makers",
        maturity: "Discovery-ready",
        pitchValue: "Shows disciplined product filtering before development.",
        isolationRule: "Only opportunity assessment, scope boundary, and validation plan are generated.",
        fields: [
          { id: "opportunityIdea", label: "Solution idea", type: "textarea", rows: 4, placeholder: "Example: Agent that helps schools respond to parent enquiries" },
          { id: "opportunityUser", label: "Target user", type: "text", placeholder: "Example: Small schools and coaching centers" },
          { id: "opportunityUrgency", label: "Problem urgency", type: "select", options: ["Low", "Medium", "High"] },
          { id: "opportunitySensitivity", label: "Data sensitivity", type: "select", options: ["Low", "Medium", "High"] },
          { id: "opportunityMonetization", label: "Possible monetization", type: "text", placeholder: "Example: Setup fee + monthly support" },
          { id: "opportunityLanguage", label: "Output language", type: "select", options: languages }
        ]
      }
    ]
  };
})();

(function () {
  const data = window.AAS_SIMULATOR_DATA;
  const engine = window.AAS_SimulatorEngine;
  const renderers = window.AAS_Renderers;

  const listEl = document.getElementById("simulatorList");
  const filtersEl = document.getElementById("categoryFilters");
  const titleEl = document.getElementById("activeTitle");
  const descEl = document.getElementById("activeDescription");
  const metaEl = document.getElementById("activeMeta");
  const fieldsEl = document.getElementById("dynamicFields");
  const form = document.getElementById("simulatorForm");
  const outputEl = document.getElementById("generatedOutput");
  const emptyEl = document.getElementById("emptyState");
  const outputShell = document.getElementById("outputShell");
  const copyBtn = document.getElementById("copyOutput");
  const jsonBtn = document.getElementById("downloadJson");
  const textBtn = document.getElementById("downloadText");
  const resetBtn = document.getElementById("resetFields");

  let selectedCategory = "All";
  let activeSimulator = null;
  let latestResult = null;

  function init() {
    if (!data || !listEl || !form) return;
    renderFilters();
    renderList();
    openSimulator(data.simulators[0].id);
    bindEvents();
  }

  function renderFilters() {
    filtersEl.innerHTML = data.categories.map((category) => `
      <button class="chip ${category === selectedCategory ? "active" : ""}" type="button" data-category="${engine.escapeHtml(category)}">${engine.escapeHtml(category)}</button>
    `).join("");
  }

  function renderList() {
    const simulators = data.simulators.filter((sim) => selectedCategory === "All" || sim.category === selectedCategory);
    listEl.innerHTML = simulators.map((sim) => `
      <button class="sim-list-item ${activeSimulator && activeSimulator.id === sim.id ? "active" : ""}" type="button" data-id="${engine.escapeHtml(sim.id)}">
        <span class="sim-icon">${sim.icon}</span>
        <span><strong>${engine.escapeHtml(sim.title)}</strong><small>${engine.escapeHtml(sim.category)} · ${engine.escapeHtml(sim.maturity)}</small></span>
      </button>
    `).join("");
  }

  function bindEvents() {
    filtersEl.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-category]");
      if (!button) return;
      selectedCategory = button.dataset.category;
      renderFilters();
      renderList();
      const firstVisible = data.simulators.find((sim) => selectedCategory === "All" || sim.category === selectedCategory);
      if (firstVisible) openSimulator(firstVisible.id);
    });

    listEl.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-id]");
      if (button) openSimulator(button.dataset.id);
    });

    form.addEventListener("change", (event) => {
      handleDependentFieldChange(event.target);
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      runSimulator();
    });

    resetBtn.addEventListener("click", () => applyDefaults(activeSimulator));
    copyBtn.addEventListener("click", () => latestResult && copyText(renderers.outputToPlainText(latestResult), copyBtn, "Copy text"));
    jsonBtn.addEventListener("click", () => latestResult && downloadBlob(renderers.outputToJson(latestResult), `${slug(latestResult.title)}.json`, "application/json"));
    textBtn.addEventListener("click", () => latestResult && downloadBlob(renderers.outputToPlainText(latestResult), `${slug(latestResult.title)}.txt`, "text/plain"));
  }

  function openSimulator(id) {
    activeSimulator = data.simulators.find((sim) => sim.id === id);
    if (!activeSimulator) return;
    titleEl.textContent = activeSimulator.title;
    descEl.textContent = activeSimulator.description;
    metaEl.innerHTML = [
      ["Buyer", activeSimulator.buyer],
      ["Maturity", activeSimulator.maturity],
      ["Pitch value", activeSimulator.pitchValue]
    ].map(([label, value]) => `<span><strong>${engine.escapeHtml(label)}:</strong> ${engine.escapeHtml(value)}</span>`).join("");
    fieldsEl.innerHTML = activeSimulator.fields.map(renderers.renderField).join("");
    applyDefaults(activeSimulator);
    latestResult = null;
    outputEl.innerHTML = "";
    emptyEl.hidden = false;
    outputShell.hidden = true;
    renderList();
  }

  function applyDefaults(simulator) {
    if (!simulator) return;
    form.reset();
    if (simulator.id === "business-page-generator") {
      const scenario = getBusinessScenario(form.elements.businessScenario.value || "Tuition Teacher");
      setValue("businessName", scenario.defaultName);
      setValue("businessLocation", scenario.defaultLocation);
      setValue("businessServices", scenario.services.join("\n"));
      setValue("businessLanguage", "Hinglish");
      setValue("businessTone", "Trust-focused");
    }
    if (simulator.id === "education-concept-tutor") {
      const topicName = form.elements.eduTopic.value || "Photosynthesis";
      const topic = data.educationTopics[topicName] || data.educationTopics.Photosynthesis;
      setValue("eduClassLevel", topic.defaultClass);
      setValue("eduStyle", "Simple");
      setValue("eduLanguage", "English");
    }
    if (simulator.id === "digital-safety-coach") {
      setValue("safetyScenario", "OTP Sharing Phone Call");
      setValue("safetyAudience", "General user");
      setValue("safetyAction", "The caller is asking me to share an OTP urgently.");
      setValue("safetyLanguage", "English");
    }
    if (simulator.id === "multi-agent-workflow-designer") {
      setValue("workflowUseCase", "Agent that drafts replies to school enquiry messages.");
      setValue("workflowDomain", "Education");
      setValue("workflowRiskLevel", "Medium");
      setValue("workflowOutputType", "Implementation blueprint");
      setValue("workflowLanguage", "English");
    }
    if (simulator.id === "solution-opportunity-evaluator") {
      setValue("opportunityIdea", "An assistant that helps schools convert parent enquiries into structured follow-up messages.");
      setValue("opportunityUser", "Small schools and coaching centers");
      setValue("opportunityUrgency", "Medium");
      setValue("opportunitySensitivity", "Medium");
      setValue("opportunityMonetization", "Setup fee plus monthly support package");
      setValue("opportunityLanguage", "English");
    }
  }

  function handleDependentFieldChange(target) {
    if (!target || !activeSimulator) return;
    if (activeSimulator.id === "business-page-generator" && target.name === "businessScenario") {
      const scenario = getBusinessScenario(target.value);
      setValue("businessName", scenario.defaultName);
      setValue("businessLocation", scenario.defaultLocation);
      setValue("businessServices", scenario.services.join("\n"));
      const serviceField = form.elements.businessServices;
      if (serviceField) serviceField.placeholder = scenario.services.join("\n");
    }
    if (activeSimulator.id === "education-concept-tutor" && target.name === "eduTopic") {
      const topic = data.educationTopics[target.value] || data.educationTopics.Photosynthesis;
      setValue("eduClassLevel", topic.defaultClass);
    }
  }

  function runSimulator() {
    const values = Object.fromEntries(new FormData(form).entries());
    latestResult = engine.generate(activeSimulator, values);
    outputEl.innerHTML = renderers.renderOutput(latestResult);
    emptyEl.hidden = true;
    outputShell.hidden = false;
  }

  function getBusinessScenario(name) {
    return data.businessScenarios[name] || data.businessScenarios["Tuition Teacher"];
  }

  function setValue(name, value) {
    const field = form.elements[name];
    if (field) field.value = value;
  }

  async function copyText(text, button, original) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (error) {
      const area = document.createElement("textarea");
      area.value = text;
      document.body.appendChild(area);
      area.select();
      document.execCommand("copy");
      area.remove();
    }
    button.textContent = "Copied";
    setTimeout(() => { button.textContent = original; }, 1200);
  }

  function downloadBlob(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  function slug(text) {
    return String(text).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 80) || "simulator-output";
  }

  document.addEventListener("DOMContentLoaded", init);
})();

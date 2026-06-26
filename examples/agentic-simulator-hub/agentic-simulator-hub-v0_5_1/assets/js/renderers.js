(function () {
  const engine = window.AAS_SimulatorEngine;

  function optionsForField(field) {
    const data = window.AAS_SIMULATOR_DATA;
    if (field.optionsFrom === "businessScenarios") return Object.keys(data.businessScenarios || {});
    if (field.optionsFrom === "educationTopics") return Object.keys(data.educationTopics || {});
    if (field.optionsFrom === "safetyScenarios") return Object.keys(data.safetyScenarios || {});
    return field.options || [];
  }

  function renderField(field) {
    const id = engine.escapeHtml(field.id);
    const label = engine.escapeHtml(field.label);
    const placeholder = engine.escapeHtml(field.placeholder || "");
    const rows = Number(field.rows || 3);
    if (field.type === "select") {
      const options = optionsForField(field).map((option) => `<option value="${engine.escapeHtml(option)}">${engine.escapeHtml(option)}</option>`).join("");
      return `<label class="field"><span>${label}</span><select id="${id}" name="${id}">${options}</select></label>`;
    }
    if (field.type === "textarea") {
      return `<label class="field field-wide"><span>${label}</span><textarea id="${id}" name="${id}" rows="${rows}" placeholder="${placeholder}"></textarea></label>`;
    }
    return `<label class="field"><span>${label}</span><input id="${id}" name="${id}" type="${engine.escapeHtml(field.type || "text")}" placeholder="${placeholder}" /></label>`;
  }

  function renderOutput(result) {
    const scoreRows = Object.entries(result.scorecard || {}).map(([label, score]) => `
      <div class="score-row">
        <div><strong>${engine.escapeHtml(label)}</strong><span>${engine.escapeHtml(engine.scoreLabel(score))}</span></div>
        <meter min="0" max="100" value="${Number(score)}"></meter>
        <b>${Number(score)}</b>
      </div>
    `).join("");

    const workflow = (result.workflow || []).map((step, index) => `<li><span>${String(index + 1).padStart(2, "0")}</span>${engine.escapeHtml(step)}</li>`).join("");
    const sections = (result.sections || []).map((section) => `<article class="output-block"><h4>${engine.escapeHtml(section.heading)}</h4>${section.html}</article>`).join("");

    return `
      <div class="output-head">
        <p class="eyebrow">${engine.escapeHtml(result.category)} · Solution preview</p>
        <h3>${engine.escapeHtml(result.title)}</h3>
        <p>${engine.escapeHtml(result.summary)}</p>
      </div>
      <div class="isolation-box"><strong>Scope boundary:</strong> ${engine.escapeHtml(result.isolationRule)}</div>
      <section class="scorecard"><h4>Readiness scorecard</h4>${scoreRows}</section>
      <section class="workflow-output"><h4>Generated workflow</h4><ol>${workflow}</ol></section>
      <section class="output-sections">${sections}</section>
      <aside class="pitch-note"><strong>Client value note:</strong> ${engine.escapeHtml(result.pitchNote)}</aside>
    `;
  }

  function outputToPlainText(result) {
    const lines = [
      result.product,
      `Version: ${result.version}`,
      `Simulator: ${result.simulatorTitle}`,
      `Title: ${result.title}`,
      "",
      result.summary,
      "",
      `Scope boundary: ${result.isolationRule}`,
      "",
      "Readiness scorecard:"
    ];
    Object.entries(result.scorecard || {}).forEach(([label, score]) => lines.push(`- ${label}: ${score}`));
    lines.push("", "Workflow:");
    (result.workflow || []).forEach((step, index) => lines.push(`${index + 1}. ${step}`));
    lines.push("", "Sections:");
    (result.sections || []).forEach((section) => {
      const text = String(section.html || "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
      lines.push(`- ${section.heading}: ${text}`);
    });
    lines.push("", `Client value note: ${result.pitchNote}`);
    return lines.join("\n");
  }

  function outputToJson(result) {
    return JSON.stringify(result, null, 2);
  }

  window.AAS_Renderers = { renderField, renderOutput, outputToPlainText, outputToJson };
})();

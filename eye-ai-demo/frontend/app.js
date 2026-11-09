(() => {
  "use strict";

  const config = Object.assign(
    {
      apiEndpoint: "/api/analyze",
      requestTimeoutMs: 165000,
      maxImageSizeMb: 10,
      maxSavedCases: 20
    },
    window.EYE_AI_CONFIG || {}
  );

  const $ = (id) => document.getElementById(id);
  const refs = {
    engineBadge: $("engineBadge"),
    historyBtn: $("historyBtn"),
    historyCount: $("historyCount"),
    patientName: $("patientName"),
    patientId: $("patientId"),
    patientAge: $("patientAge"),
    eyeSide: $("eyeSide"),
    patientSex: $("patientSex"),
    dropZone: $("dropZone"),
    fileInput: $("fileInput"),
    cameraInput: $("cameraInput"),
    browseBtn: $("browseBtn"),
    cameraBtn: $("cameraBtn"),
    emptyUploadState: $("emptyUploadState"),
    previewState: $("previewState"),
    previewImage: $("previewImage"),
    fileName: $("fileName"),
    fileInfo: $("fileInfo"),
    qualityChip: $("qualityChip"),
    qualityWarnings: $("qualityWarnings"),
    removeImageBtn: $("removeImageBtn"),
    consentCheck: $("consentCheck"),
    analyzeBtn: $("analyzeBtn"),
    analysisProgress: $("analysisProgress"),
    progressTitle: $("progressTitle"),
    progressPercent: $("progressPercent"),
    progressBar: $("progressBar"),
    resultsSection: $("resultsSection"),
    resultTimestamp: $("resultTimestamp"),
    resultModeBadge: $("resultModeBadge"),
    demoWarning: $("demoWarning"),
    summaryBanner: $("summaryBanner"),
    summaryTitle: $("summaryTitle"),
    summaryText: $("summaryText"),
    drEngine: $("drEngine"),
    drGradeCircle: $("drGradeCircle"),
    drGrade: $("drGrade"),
    drLabel: $("drLabel"),
    drConfidence: $("drConfidence"),
    drConfidenceValue: $("drConfidenceValue"),
    drConfidenceBar: $("drConfidenceBar"),
    drScale: $("drScale"),
    amdEngine: $("amdEngine"),
    amdStatus: $("amdStatus"),
    amdProbability: $("amdProbability"),
    amdConfidenceBar: $("amdConfidenceBar"),
    glEngine: $("glEngine"),
    glStatus: $("glStatus"),
    glProbability: $("glProbability"),
    glConfidenceBar: $("glConfidenceBar"),
    nextStepText: $("nextStepText"),
    saveBtn: $("saveBtn"),
    printBtn: $("printBtn"),
    downloadJsonBtn: $("downloadJsonBtn"),
    newAnalysisBtn: $("newAnalysisBtn"),
    historyDialog: $("historyDialog"),
    closeHistoryBtn: $("closeHistoryBtn"),
    historyEmpty: $("historyEmpty"),
    historyList: $("historyList"),
    exportAllBtn: $("exportAllBtn"),
    clearHistoryBtn: $("clearHistoryBtn"),
    printReport: $("printReport"),
    toast: $("toast")
  };

  const DR_LABELS = [
    "لا توجد علامات ظاهرة",
    "اعتلال خفيف",
    "اعتلال متوسط",
    "اعتلال شديد",
    "اعتلال تكاثري / متقدم"
  ];

  const STORAGE_KEY = "eye_ai_retfound_cases_v2";
  const state = {
    selectedFile: null,
    objectUrl: null,
    imageDataUrl: "",
    quality: null,
    result: null,
    cases: loadCases(),
    analyzing: false,
    loading: false
  };

  let toastTimer = null;

  function init() {
    bindEvents();
    updateAnalyzeButton();
    renderHistory();
    setEngineBadge("disconnected");
    checkConnection();
  }

  function bindEvents() {
    refs.browseBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      refs.fileInput.click();
    });
    refs.cameraBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      refs.cameraInput.click();
    });
    refs.fileInput.addEventListener("change", () => refs.fileInput.files[0] && handleFile(refs.fileInput.files[0]));
    refs.cameraInput.addEventListener("change", () => refs.cameraInput.files[0] && handleFile(refs.cameraInput.files[0]));
    refs.removeImageBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      clearImage();
    });
    refs.dropZone.addEventListener("click", (event) => {
      if (event.target === refs.dropZone || event.target.closest(".empty-upload h3, .empty-upload p, .upload-icon")) {
        refs.fileInput.click();
      }
    });
    refs.dropZone.addEventListener("keydown", (event) => {
      if ((event.key === "Enter" || event.key === " ") && event.target === refs.dropZone) {
        event.preventDefault();
        refs.fileInput.click();
      }
    });
    ["dragenter", "dragover"].forEach((type) => refs.dropZone.addEventListener(type, (event) => {
      event.preventDefault();
      refs.dropZone.classList.add("drag-over");
    }));
    ["dragleave", "drop"].forEach((type) => refs.dropZone.addEventListener(type, (event) => {
      event.preventDefault();
      refs.dropZone.classList.remove("drag-over");
    }));
    refs.dropZone.addEventListener("drop", (event) => {
      const file = event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0];
      if (file) handleFile(file);
    });

    refs.consentCheck.addEventListener("change", updateAnalyzeButton);
    refs.analyzeBtn.addEventListener("click", analyzeCurrentImage);
    refs.saveBtn.addEventListener("click", saveCurrentCase);
    refs.printBtn.addEventListener("click", printCurrentReport);
    refs.downloadJsonBtn.addEventListener("click", () => state.result && downloadJson(buildExportRecord(), `eye-ai-${safeFilename(state.result.analysis_id)}.json`));
    refs.newAnalysisBtn.addEventListener("click", resetForNewAnalysis);

    refs.historyBtn.addEventListener("click", openHistory);
    refs.closeHistoryBtn.addEventListener("click", () => refs.historyDialog.close());
    refs.historyDialog.addEventListener("click", (event) => {
      const rect = refs.historyDialog.getBoundingClientRect();
      const outside = event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom;
      if (outside) refs.historyDialog.close();
    });
    refs.historyList.addEventListener("click", handleHistoryAction);
    refs.exportAllBtn.addEventListener("click", () => {
      if (!state.cases.length) return showToast("لا توجد حالات لتصديرها.");
      downloadJson({ exported_at: new Date().toISOString(), cases: state.cases }, `eye-ai-history-${dateStamp()}.json`);
    });
    refs.clearHistoryBtn.addEventListener("click", clearAllCases);
  }

  async function handleFile(file) {
    if (!file || state.analyzing || state.loading) return;
    const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
    const maxBytes = config.maxImageSizeMb * 1024 * 1024;

    if (!allowedTypes.includes(file.type)) {
      showToast("الصيغة غير مدعومة. استخدم JPG أو PNG أو WEBP.");
      return;
    }
    if (file.size > maxBytes) {
      showToast(`حجم الصورة أكبر من ${config.maxImageSizeMb} ميغابايت.`);
      return;
    }

    $("analysisError").hidden = true;
    state.loading = true;
    state.result = null;
    updateAnalyzeButton();
    if (state.objectUrl) URL.revokeObjectURL(state.objectUrl);
    state.selectedFile = file;
    state.objectUrl = URL.createObjectURL(file);
    state.imageDataUrl = "";
    state.result = null;
    refs.resultsSection.hidden = true;
    refs.emptyUploadState.hidden = true;
    refs.previewState.hidden = false;
    refs.previewImage.src = state.objectUrl;
    refs.fileName.textContent = file.name || "صورة العين";
    refs.fileInfo.textContent = `${formatBytes(file.size)} • جاري قراءة الأبعاد`;
    refs.qualityChip.className = "quality-chip";
    refs.qualityChip.textContent = "جارٍ فحص الجودة…";
    refs.qualityWarnings.replaceChildren();

    try {
      await waitForImage(refs.previewImage);
      state.quality = assessImageQuality(refs.previewImage);
      refs.fileInfo.textContent = `${formatBytes(file.size)} • ${refs.previewImage.naturalWidth} × ${refs.previewImage.naturalHeight}`;
      renderQuality(state.quality);
      state.imageDataUrl = await makeThumbnail(refs.previewImage, 760, 0.86);
    } catch (error) {
      console.error(error);
      state.loading = false;
      clearImage();
      showToast("تعذر قراءة الصورة. جرّب ملفًا آخر.");
      return;
    }
    state.loading = false;
    updateAnalyzeButton();
  }

  function clearImage() {
    if (state.analyzing || state.loading) return;
    if (state.objectUrl) URL.revokeObjectURL(state.objectUrl);
    state.selectedFile = null;
    state.objectUrl = null;
    state.imageDataUrl = "";
    state.quality = null;
    state.result = null;
    refs.previewImage.removeAttribute("src");
    refs.emptyUploadState.hidden = false;
    refs.previewState.hidden = true;
    refs.resultsSection.hidden = true;
    refs.analysisProgress.hidden = true;
    $("analysisError").hidden = true;
    refs.fileInput.value = "";
    refs.cameraInput.value = "";
    updateAnalyzeButton();
  }

  function updateAnalyzeButton() {
    refs.analyzeBtn.disabled = !state.selectedFile || !refs.consentCheck.checked || state.analyzing || state.loading;
  }

  function assessImageQuality(image) {
    const canvas = document.createElement("canvas");
    const size = 128;
    canvas.width = size;
    canvas.height = size;
    const context = canvas.getContext("2d", { willReadFrequently: true });
    context.drawImage(image, 0, 0, size, size);
    const pixels = context.getImageData(0, 0, size, size).data;
    let sum = 0;
    let sumSq = 0;
    let active = 0;

    for (let index = 0; index < pixels.length; index += 16) {
      const alpha = pixels[index + 3];
      if (alpha < 20) continue;
      const luminance = 0.2126 * pixels[index] + 0.7152 * pixels[index + 1] + 0.0722 * pixels[index + 2];
      sum += luminance;
      sumSq += luminance * luminance;
      active += 1;
    }

    const brightness = active ? sum / active : 0;
    const variance = active ? Math.max(0, sumSq / active - brightness * brightness) : 0;
    const contrast = Math.sqrt(variance);
    const minSide = Math.min(image.naturalWidth, image.naturalHeight);
    const warnings = [];
    let score = 100;

    if (minSide < 512) {
      score -= 28;
      warnings.push("الدقة منخفضة؛ يفضّل أن يكون أقصر ضلع 512 بكسل على الأقل.");
    } else if (minSide < 900) {
      score -= 10;
      warnings.push("الدقة مقبولة، لكن صورة أعلى دقة قد تعطي نتيجة أفضل.");
    }
    if (brightness < 42) {
      score -= 30;
      warnings.push("الصورة مظلمة جدًا؛ أعد التصوير بإضاءة مناسبة.");
    } else if (brightness > 218) {
      score -= 30;
      warnings.push("الصورة ساطعة جدًا وقد تحتوي على مناطق محروقة.");
    } else if (brightness < 62 || brightness > 195) {
      score -= 12;
      warnings.push("سطوع الصورة ليس مثاليًا.");
    }
    if (contrast < 22) {
      score -= 25;
      warnings.push("التباين منخفض؛ قد تكون الصورة ضبابية أو غير واضحة.");
    } else if (contrast < 32) {
      score -= 10;
      warnings.push("التباين متوسط؛ تأكد من وضوح تفاصيل الشبكية.");
    }

    score = Math.max(0, Math.min(100, Math.round(score)));
    const level = score >= 78 ? "good" : score >= 52 ? "fair" : "poor";
    return {
      score,
      level,
      brightness: Number(brightness.toFixed(1)),
      contrast: Number(contrast.toFixed(1)),
      width: image.naturalWidth,
      height: image.naturalHeight,
      warnings
    };
  }

  function renderQuality(quality) {
    const labels = { good: "جودة جيدة", fair: "جودة مقبولة", poor: "جودة ضعيفة" };
    refs.qualityChip.className = `quality-chip quality-${quality.level}`;
    refs.qualityChip.textContent = `${labels[quality.level]} • ${quality.score}%`;
    refs.qualityWarnings.replaceChildren();
    quality.warnings.forEach((warning) => {
      const item = document.createElement("li");
      item.textContent = warning;
      refs.qualityWarnings.appendChild(item);
    });
  }

  async function checkConnection() {
    try {
      const response = await fetch("/api/health", { signal: AbortSignal.timeout(12000) });
      if (!response.ok) throw new Error("not ready");
      const health = await response.json();
      if (health.status !== "ready" || health.mode !== "retfound") throw new Error("not ready");
      setEngineBadge("retfound");
      $("connectionStatus").textContent = `متصل بـ RETFound • ${health.model.device} • ${health.model.dtype}`;
    } catch (_) {
      setEngineBadge("disconnected");
      $("connectionStatus").textContent = "تعذر التحقق من الاتصال. شغّل خادم RETFound ثم أعد تحميل الصفحة. لن تُستخدم المحاكاة.";
    }
  }

  async function analyzeCurrentImage() {
    if (!state.selectedFile || !refs.consentCheck.checked || state.analyzing || state.loading) return;
    state.analyzing = true;
    state.result = null;
    updateAnalyzeButton();
    refs.resultsSection.hidden = true;
    $("analysisError").hidden = true;
    refs.analysisProgress.hidden = false;
    refs.previewImage.closest(".preview-frame").classList.add("scanning");
    try {
      setProgress(15, "إرسال الصورة الأصلية إلى Jev ثم RETFound…", 1);
      const result = await requestAnalysis(state.selectedFile);
      state.result = normalizeResult(result);
      setProgress(100, "اكتمل استدلال RETFound", 3);
      renderResult(state.result);
      refs.resultsSection.hidden = false;
      refs.resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      state.result = null;
      $("analysisError").textContent = error.message || "تعذر إكمال التحليل. لم تُنتج نتيجة.";
      $("analysisError").hidden = false;
    } finally {
      refs.analysisProgress.hidden = true;
      refs.previewImage.closest(".preview-frame").classList.remove("scanning");
      state.analyzing = false;
      updateAnalyzeButton();
    }
  }

  function setProgress(percent, title, step) {
    refs.progressPercent.textContent = `${percent}%`;
    refs.progressBar.style.width = `${percent}%`;
    refs.progressTitle.textContent = title;
    document.querySelectorAll("[data-progress-step]").forEach((element) => {
      element.classList.toggle("active", Number(element.dataset.progressStep) <= step);
    });
  }

  async function requestAnalysis(file) {
    if (location.protocol === "file:") throw new Error("شغّل run_demo.py وافتح http://127.0.0.1:8001 بدل فتح الملف مباشرة.");
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.requestTimeoutMs);
    try {
      const formData = new FormData();
      formData.append("file", file, file.name || "retina.jpg");
      const response = await fetch(config.apiEndpoint, {
        method: "POST", body: formData, signal: controller.signal,
        headers: { Accept: "application/json" }
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(typeof payload.detail === "string" ? payload.detail : `فشل الطلب (${response.status}).`);
      return payload;
    } catch (error) {
      if (error.name === "AbortError") throw new Error("انتهت مهلة الاتصال؛ قد يكون الطلب نُفّذ. لا توجد إعادة محاولة تلقائية.");
      if (error instanceof TypeError) throw new Error("تعذر الاتصال بخادم الديمو. لم تُنتج نتيجة بديلة.");
      throw error;
    } finally {
      clearTimeout(timeout);
    }
  }

  function normalizeResult(result) {
    return window.EyeAIContract.normalize(result, state.quality);
  }

  function renderResult(result) {
    const dr = result.models.diabetic_retinopathy;
    const amd = result.models.amd;
    const glaucoma = result.models.glaucoma;
    const date = new Date(result.timestamp);

    refs.resultTimestamp.textContent = `${formatArabicDate(date)} • رقم التحليل ${result.analysis_id}`;
    setResultModeBadge(result.mode);
    refs.demoWarning.hidden = false;
    setEngineBadge(result.mode);

    const summary = createSummary(dr, amd, glaucoma);
    refs.summaryBanner.className = `summary-banner ${summary.level === "normal" ? "" : summary.level}`.trim();
    refs.summaryBanner.querySelector(".summary-symbol").textContent = summary.level === "normal" ? "✓" : summary.level === "warning" ? "!" : "+";
    refs.summaryTitle.textContent = summary.title;
    refs.summaryText.textContent = summary.text;
    refs.nextStepText.textContent = summary.nextStep;

    renderEngineTag(refs.drEngine, dr.engine);
    refs.drGrade.textContent = String(dr.grade);
    refs.drLabel.textContent = dr.label_ar;
    refs.drConfidence.textContent = `أعلى درجة نموذج غير معايرة: ${formatPercent(dr.confidence)}`;
    refs.drConfidenceValue.textContent = formatPercent(dr.confidence);
    refs.drConfidenceBar.style.width = `${dr.confidence * 100}%`;
    refs.drGradeCircle.style.background = `conic-gradient(${gradeColor(dr.grade)} 0 ${(dr.grade + 1) * 20}%, #e6eeee ${(dr.grade + 1) * 20}% 100%)`;
    refs.drScale.querySelectorAll("[data-grade]").forEach((element) => element.classList.toggle("active", Number(element.dataset.grade) === dr.grade));

    $("drScores").replaceChildren();
    dr.probabilities.forEach((score, grade) => {
      const row = document.createElement("li");
      row.textContent = `${grade} — ${DR_LABELS[grade]}: ${(score * 100).toFixed(2)}%`;
      $("drScores").appendChild(row);
    });
    const identity = result.source_prediction.model;
    $("modelIdentity").textContent = `الجهاز: ${identity.device} • ${identity.dtype} • المعالجة: ${identity.preprocessing_version} • SHA-256: ${identity.checkpoint_sha256}`;
    renderEngineTag(refs.amdEngine, amd.engine);
    renderBinaryStatus(refs.amdStatus, null);
    refs.amdProbability.textContent = "غير متاح";
    refs.amdConfidenceBar.style.width = "0%";

    renderEngineTag(refs.glEngine, glaucoma.engine);
    renderBinaryStatus(refs.glStatus, null);
    refs.glProbability.textContent = "غير متاح";
    refs.glConfidenceBar.style.width = "0%";
  }

  function createSummary(dr) {
    return {
      level: dr.grade >= 3 ? "alert" : dr.grade > 0 ? "warning" : "normal",
      title: `تصنيف RETFound: ${DR_LABELS[dr.grade]} (الدرجة ${dr.grade})`,
      text: "هذه نتيجة بحثية لاعتلال الشبكية السكري فقط. لم يتم تقييم AMD أو الجلوكوما، والدرجات غير معايرة سريريًا.",
      nextStep: "تحتاج النتيجة إلى تفسير اختصاصي عيون ولا تُعد تشخيصًا طبيًا."
    };
  }

  function renderBinaryStatus(container) {
    container.classList.remove("positive");
    container.querySelector("strong").textContent = "لم يتم التقييم — لا يوجد موديل لهذا المرض";
  }

  function renderEngineTag(element, engine) {
    element.className = `engine-tag ${engine === "retfound" ? "live" : "demo"}`;
    element.textContent = engine === "retfound" ? "RETFound الحقيقي" : "غير متاح";
  }

  function setEngineBadge(mode) {
    refs.engineBadge.className = `badge ${mode === "retfound" ? "badge-live" : "badge-demo"}`;
    refs.engineBadge.textContent = mode === "retfound" ? "متصل بـ RETFound" : "الاتصال غير متحقق";
  }

  function setResultModeBadge() {
    refs.resultModeBadge.className = "badge badge-live";
    refs.resultModeBadge.textContent = "نتيجة RETFound فعلية";
  }

  async function saveCurrentCase() {
    if (!state.result || state.analyzing || state.loading) return;
    let imageData = state.imageDataUrl;
    if (!imageData && refs.previewImage.src) {
      try { imageData = await makeThumbnail(refs.previewImage, 520, 0.76); } catch (_) { imageData = ""; }
    }

    const record = {
      id: state.result.analysis_id,
      saved_at: new Date().toISOString(),
      patient: getPatientData(),
      image_data_url: imageData,
      result: state.result
    };

    const existingIndex = state.cases.findIndex((item) => item.id === record.id);
    if (existingIndex >= 0) state.cases.splice(existingIndex, 1);
    state.cases.unshift(record);
    state.cases = state.cases.slice(0, config.maxSavedCases);

    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.cases));
    } catch (error) {
      console.warn("Storage quota reached. Retrying without images.", error);
      state.cases = state.cases.map((item) => ({ ...item, image_data_url: "" }));
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state.cases));
      } catch (secondError) {
        console.error(secondError);
        showToast("تعذر الحفظ؛ مساحة التخزين المحلية ممتلئة.");
        return;
      }
    }

    renderHistory();
    showToast("تم حفظ الحالة على هذا الجهاز.");
  }

  function loadCases() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(parsed) ? parsed.filter(record => {
        try { window.EyeAIContract.normalize(record.result, null); return true; } catch (_) { return false; }
      }).slice(0, config.maxSavedCases) : [];
    } catch (_) {
      return [];
    }
  }

  function renderHistory() {
    refs.historyCount.textContent = String(state.cases.length);
    refs.historyEmpty.hidden = state.cases.length > 0;
    refs.historyList.hidden = state.cases.length === 0;
    refs.historyList.replaceChildren();

    state.cases.forEach((record) => {
      const item = document.createElement("article");
      item.className = "history-item";
      item.dataset.caseId = record.id;

      const image = document.createElement("img");
      image.className = "history-thumb";
      image.alt = "صورة الحالة المحفوظة";
      image.src = record.image_data_url || "assets/logo.svg";

      const info = document.createElement("div");
      info.className = "history-info";
      const title = document.createElement("h3");
      title.textContent = record.patient && record.patient.name ? record.patient.name : "حالة بدون اسم";
      const meta = document.createElement("p");
      meta.textContent = `${formatArabicDate(new Date(record.saved_at || record.result.timestamp))} • ${record.id}`;
      const chips = document.createElement("div");
      chips.className = "history-chips";
      const dr = record.result.models.diabetic_retinopathy;
      const amd = record.result.models.amd;
      const gl = record.result.models.glaucoma;
      [
        `DR ${dr.grade}`,
        "AMD غير مقيّم",
        "GL غير مقيّم"
      ].forEach((text) => {
        const chip = document.createElement("span");
        chip.textContent = text;
        chips.appendChild(chip);
      });
      info.append(title, meta, chips);

      const actions = document.createElement("div");
      actions.className = "history-actions";
      actions.append(
        actionButton("فتح", "open", "btn btn-secondary"),
        actionButton("PDF", "print", "btn btn-ghost"),
        actionButton("حذف", "delete", "btn btn-danger")
      );
      item.append(image, info, actions);
      refs.historyList.appendChild(item);
    });
  }

  function actionButton(label, action, className) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.dataset.action = action;
    button.textContent = label;
    return button;
  }

  function openHistory() {
    renderHistory();
    if (typeof refs.historyDialog.showModal === "function") refs.historyDialog.showModal();
    else refs.historyDialog.setAttribute("open", "");
  }

  function handleHistoryAction(event) {
    if (state.analyzing || state.loading) return;
    const button = event.target.closest("button[data-action]");
    const item = event.target.closest("[data-case-id]");
    if (!button || !item) return;
    const record = state.cases.find((entry) => entry.id === item.dataset.caseId);
    if (!record) return;

    if (button.dataset.action === "delete") {
      state.cases = state.cases.filter((entry) => entry.id !== record.id);
      persistCases();
      renderHistory();
      showToast("تم حذف الحالة.");
      return;
    }

    loadRecordIntoView(record);
    refs.historyDialog.close();
    if (button.dataset.action === "print") {
      setTimeout(printCurrentReport, 100);
    }
  }

  function loadRecordIntoView(record) {
    const patient = record.patient || {};
    refs.patientName.value = patient.name || "";
    refs.patientId.value = patient.id || "";
    refs.patientAge.value = patient.age || "";
    refs.eyeSide.value = patient.eye_side || "غير محددة";
    refs.patientSex.value = patient.sex || "غير محدد";
    state.result = normalizeResult(record.result);
    state.imageDataUrl = record.image_data_url || "";
    state.quality = state.result.quality;
    state.selectedFile = null;
    if (record.image_data_url) {
      refs.previewImage.src = record.image_data_url;
      refs.fileName.textContent = `حالة محفوظة — ${record.id}`;
      refs.fileInfo.textContent = "صورة محفوظة محليًا";
      refs.emptyUploadState.hidden = true;
      refs.previewState.hidden = false;
      renderQuality(state.quality);
    } else {
      refs.previewImage.removeAttribute("src");
      refs.emptyUploadState.hidden = false;
      refs.previewState.hidden = true;
    }
    renderResult(state.result);
    refs.resultsSection.hidden = false;
    refs.resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    updateAnalyzeButton();
  }

  function persistCases() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state.cases)); } catch (error) { console.error(error); }
    refs.historyCount.textContent = String(state.cases.length);
  }

  function clearAllCases() {
    if (!state.cases.length) return showToast("السجل فارغ بالفعل.");
    if (!window.confirm("هل تريد حذف جميع الحالات المحفوظة من هذا الجهاز؟")) return;
    state.cases = [];
    persistCases();
    renderHistory();
    showToast("تم حذف جميع الحالات.");
  }

  function printCurrentReport() {
    if (!state.result || state.analyzing || state.loading) return;
    populatePrintReport();
    setTimeout(() => window.print(), 100);
  }

  function populatePrintReport() {
    const result = state.result;
    const patient = getPatientData();
    const dr = result.models.diabetic_retinopathy;
    const amd = result.models.amd;
    const glaucoma = result.models.glaucoma;
    const summary = createSummary(dr, amd, glaucoma);

    $("reportId").textContent = result.analysis_id;
    $("reportDate").textContent = formatArabicDate(new Date(result.timestamp));
    $("reportPatientName").textContent = patient.name || "غير مسجل";
    $("reportPatientId").textContent = patient.id || "غير مسجل";
    $("reportPatientAge").textContent = patient.age ? `${patient.age} سنة` : "غير مسجل";
    $("reportEyeSide").textContent = patient.eye_side || "غير محددة";
    $("reportImage").src = state.imageDataUrl || refs.previewImage.src || "assets/logo.svg";
    $("reportDr").textContent = `الدرجة ${dr.grade}/4 — ${dr.label_ar}`;
    $("reportDrConf").textContent = `درجة النموذج غير المعايرة ${formatPercent(dr.confidence)} • RETFound`;
    $("reportAmd").textContent = "لم يتم التقييم — لا يوجد موديل";
    $("reportAmdConf").textContent = "غير متاح";
    $("reportGl").textContent = "لم يتم التقييم — لا يوجد موديل";
    $("reportGlConf").textContent = "غير متاح";
    $("reportSummary").textContent = `${summary.title}. ${summary.text} ${summary.nextStep}`;
    $("reportMode").textContent = "RETFound الحقيقي • Jev ثم تصنيف DR فقط";
    $("reportProvenance").textContent = $("modelIdentity").textContent;
    $("reportQuality").textContent = `${qualityLabel(result.quality.level)} (${result.quality.score}%)`;
  }

  function buildExportRecord() {
    return {
      schema_version: "1.0",
      exported_at: new Date().toISOString(),
      patient: getPatientData(),
      result: state.result,
      disclaimer_ar: "هذه النتيجة تجريبية ولا تعد تشخيصًا طبيًا ويجب تأكيدها بواسطة اختصاصي عيون."
    };
  }

  function getPatientData() {
    return {
      name: refs.patientName.value.trim(),
      id: refs.patientId.value.trim(),
      age: refs.patientAge.value ? Number(refs.patientAge.value) : null,
      eye_side: refs.eyeSide.value,
      sex: refs.patientSex.value
    };
  }

  function resetForNewAnalysis() {
    clearImage();
    refs.consentCheck.checked = false;
    window.scrollTo({ top: refs.dropZone.getBoundingClientRect().top + window.scrollY - 30, behavior: "smooth" });
  }

  function makeThumbnail(image, maxSize = 600, quality = 0.8) {
    const scale = Math.min(1, maxSize / Math.max(image.naturalWidth || image.width, image.naturalHeight || image.height));
    const width = Math.max(1, Math.round((image.naturalWidth || image.width) * scale));
    const height = Math.max(1, Math.round((image.naturalHeight || image.height) * scale));
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext("2d");
    context.drawImage(image, 0, 0, width, height);
    return canvas.toDataURL("image/jpeg", quality);
  }

  function waitForImage(image) {
    if (image.complete && image.naturalWidth) return Promise.resolve();
    return new Promise((resolve, reject) => {
      image.addEventListener("load", resolve, { once: true });
      image.addEventListener("error", reject, { once: true });
    });
  }

  function downloadJson(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function showToast(message) {
    clearTimeout(toastTimer);
    refs.toast.textContent = message;
    refs.toast.classList.add("show");
    toastTimer = setTimeout(() => refs.toast.classList.remove("show"), 2800);
  }

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes)) return "—";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  }

  function formatPercent(value) {
    return `${Math.round(clamp(value, 0, 1) * 100)}%`;
  }

  function formatArabicDate(date) {
    try {
      return new Intl.DateTimeFormat("ar", { dateStyle: "medium", timeStyle: "short" }).format(date);
    } catch (_) {
      return date.toLocaleString();
    }
  }

  function dateStamp() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
  }

  function safeFilename(value) {
    return String(value || "report").replace(/[^a-zA-Z0-9_-]+/g, "-").slice(0, 80);
  }

  function gradeColor(grade) {
    return ["#58a989", "#91b95f", "#e5aa48", "#df7e42", "#c64b52"][grade] || "#0b6b76";
  }

  function qualityLabel(level) {
    return level === "unknown" ? "غير متاحة" : level === "good" ? "جيدة" : level === "fair" ? "مقبولة" : "ضعيفة";
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  init();
  window.eyeAiDemo = { state, requestAnalysis, normalizeResult, assessImageQuality };
})();

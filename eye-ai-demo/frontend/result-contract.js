(function (root) {
  "use strict";
  function normalize(result, quality) {
    const dr = result?.models?.diabetic_retinopathy;
    const source = result?.source_prediction;
    const scores = dr?.probabilities;
    if (result?.mode !== "retfound" || dr?.engine !== "retfound" ||
        !Number.isInteger(dr.grade) || dr.grade < 0 || dr.grade > 4 ||
        !Array.isArray(scores) || scores.length !== 5 ||
        scores.some(s => typeof s !== "number" || !Number.isFinite(s) || s < 0 || s > 1) ||
        Math.abs(scores.reduce((a, b) => a + b, 0) - 1) > 0.0001 ||
        scores.indexOf(Math.max(...scores)) !== dr.grade || dr.confidence !== scores[dr.grade] ||
        source?.schema_version !== "retfound-prediction/1" ||
        source.predicted_grade !== dr.grade || JSON.stringify(source.scores) !== JSON.stringify(scores) ||
        source.request_id !== result.analysis_id || source.created_utc !== result.timestamp ||
        source.input_validation?.status !== "accepted" || source.input_validation?.decision !== 1 ||
        !source.model?.checkpoint_sha256 || !source.model?.preprocessing_version ||
        !source.model?.device || !source.model?.dtype ||
        result.models.amd?.available !== false || result.models.glaucoma?.available !== false) {
      throw new Error("النتيجة غير متوافقة مع RETFound. لن تُعرض نتيجة افتراضية أو محاكاة.");
    }
    return { ...result, quality: result.quality || quality || { score: 0, level: "unknown", warnings: [] } };
  }
  root.EyeAIContract = { normalize };
  if (typeof module !== "undefined") module.exports = { normalize };
})(typeof window !== "undefined" ? window : globalThis);

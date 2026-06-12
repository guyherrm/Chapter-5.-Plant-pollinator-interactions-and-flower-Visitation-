# =========================
# Load packages
# =========================
library(lme4)
library(lmerTest)
library(MuMIn)

# Required for R² stability
options(na.action = "na.fail")

# =========================
# Load data
# =========================
df <- read.csv("../model_df.csv")

# =========================
# Predictors
# =========================
predictors <- c(
  "time_since_last_minutes",
  "clock_time",
  "max_seq",
  "visit_sequence",
  "last_visit_time"
)

predictor_seq <- paste(predictors, collapse = " + ")

# =========================
# Model formula (nested random effects)
# =========================
formula <- as.formula(
  paste("time ~", predictor_seq, "+ (1 | data_point/flower_code)")
)

# =========================
# Fit model
# =========================
model <- lmer(formula, data = df)

# =========================
# Model summary
# =========================
print(summary(model))

# =========================
# Confidence intervals (95%)
# =========================
ci <- confint(model, method = "Wald")
print(ci)

# =========================
# Fixed effects + p-values
# =========================
coefs <- summary(model)$coefficients

pvals <- coefs[, "Pr(>|t|)"]
pvals_bonf <- p.adjust(pvals, method = "bonferroni")

results <- data.frame(
  Estimate = fixef(model),
  Std_Error = coefs[, "Std. Error"],
  t_value = coefs[, "t value"],
  p_value = pvals,
  p_value_bonf = pvals_bonf
)

print(results)

# =========================
# R² (variance explained)
# =========================
r2 <- r.squaredGLMM(model)

r2_table <- data.frame(
  R2_marginal = r2[1],
  R2_conditional = r2[2]
)

print(r2_table)

model_metrics <- data.frame(
  AIC = AIC(model),
  BIC = BIC(model),
  logLik = logLik(model)
)

print(model_metrics)
# =========================
# Save outputs
# =========================
write.csv(
  results,
  "results/lmm_results.csv",
  row.names = TRUE
)

write.csv(
  ci,
  "../results/lmm_confint.csv"
)

write.csv(
  r2_table,
  "results/lmm_r2.csv",
  row.names = FALSE
)

cat("\nDONE: LMM complete\n")


library(lme4)
library(lmerTest)
library(MuMIn)

options(na.action = "na.fail")


df <- read.csv("../model_df.csv")

predictors <- c(
  "time_since_last_minutes",
  "clock_time",
  "max_seq",
  "visit_sequence",
  "last_visit_time"
)

predictor_seq <- paste(predictors, collapse = " + ")


formula <- as.formula(
  paste("time ~", predictor_seq, "+ (1 | data_point/flower_code)") # nested random effects
)


model <- lmer(formula, data = df) #model fit


print(summary(model)) #summary


ci <- confint(model, method = "Wald") #confidence intervals
print(ci)


coefs <- summary(model)$coefficients # fixed effect coefficients

pvals <- coefs[, "Pr(>|t|)"]
pvals_bonf <- p.adjust(pvals, method = "bonferroni") #did boneferroni adjustment (not used)

results <- data.frame(
  Estimate = fixef(model),
  Std_Error = coefs[, "Std. Error"],
  t_value = coefs[, "t value"],
  p_value = pvals,
  p_value_bonf = pvals_bonf
)

print(results)


r2 <- r.squaredGLMM(model)#Var explained

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

#Save the outputs

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

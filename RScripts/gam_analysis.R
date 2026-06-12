
library(mgcv)


df <- read.csv("../model_df.csv")

model <- gam(
  time ~ 
    s(time_since_last_minutes, k = 15) +
    s(clock_time, k = 15) +
    s(max_seq, k = 10) +
    s(visit_sequence, k = 10) +
    s(last_visit_time, k = 15) +

    # random effects (hierarchical structure)
    s(data_point, bs = "re") +
    s(flower_code, bs = "re"),

  data = df,
  method = "REML"
)

#Output of model
summary(model)

# Diagnose model
gam.check(model)

par(mfrow = c(2,2))
plot(model, pages = 1, shade = TRUE)

# collect results
gam_summary <- summary(model)

parametric_table <- gam_summary$p.table
smooth_table <- gam_summary$s.table

print(parametric_table)
print(smooth_table)


model_metrics <- data.frame(
  AIC = AIC(model),
  BIC = BIC(model),
  logLik = logLik(model)
)

print(model_metrics)

# save results
write.csv(
  parametric_table,
  "results/gam_parametric_results.csv",
  row.names = TRUE
)

write.csv(
  smooth_table,
  "../results/gam_smooth_results.csv",
  row.names = TRUE
)

cat("\nDONE: Fixed GAM model complete\n")

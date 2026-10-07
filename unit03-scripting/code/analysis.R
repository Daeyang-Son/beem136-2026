library(fixest)

mroz <- read.csv("data/mroz.csv")
workers <- subset(mroz, inlf == 1)
summary(workers$wage)

model <- feols(lwage ~ educ + exper + expersq, data = workers, vcov = "hetero")
summary(model)

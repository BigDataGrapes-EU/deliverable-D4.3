library(dplyr)
library(tidyr)
library(purrr)
library(ggplot2)
library(jsonlite)
# library(rmse)

data.raw = read.csv("Datasets/food_dataset_original.csv")
data.product.names = as.character(droplevels(data.raw$product))
Encoding(data.product.names) = "UTF-8"
data.raw$product = data.product.names

# Save data as csv and json
save.csv = function(data, name) {
  write.csv(
    x = data,
    file = name,
    row.names = FALSE,
    quote = FALSE
  )
}
save.json = function(data, name) {
  stream_out(data, file(name))
}

# Expand date json
data = data.raw %>%
  mutate(priceDate = gsub("'", "\"", as.character(data.raw$priceDate))) %>%
  mutate(json = map(priceDate, ~ fromJSON(.) %>% as.data.frame())) %>%
  unnest(json)
data = data %>%
  select(product, country, price, millisSinceEpoch) %>%
  filter(country != "")
data$price = as.numeric(data$price)
save.csv(data, "Datasets/food_dataset.csv")

# Prepare data for regression
make.regressable = function(data, n) {
  millis = data$millisSinceEpoch
  last = millis[length(millis)]
  dates.future = seq(
    as.POSIXct(last / 1000, origin = "1970-01-01", tz = 'UTC'),
    by = 'months',
    length = n + 1
  )
  millis.future = as.numeric(dates.future[2:(n + 1)]) * 1000
  to.regress = data.frame(millisSinceEpoch = millis.future, price = NA) %>%
    mutate(country = rep(data.frame(data$country)[1,], n)) %>%
    mutate(product = as.character(rep(data.frame(data$product)[1,], n)))
  data.new = bind_rows(data, to.regress)
  return(data.new)
}

# Compute predictions for product data
predict.product = function(data, levels, degree, n, type) {
  countries = unique(data$country)
  data.predicted = data.frame()
  for (c in countries) {
    data.country = data %>% filter(country == c)
    prediction = predict.country(data.country, levels, degree, n, type)
    if (!is.null(prediction)) {
      data.predicted = bind_rows(data.predicted, prediction)
    }
  }
  return(data.predicted)
}

# Compute predictions for product country data
predict.country = function(data, levels, degree, n, type) {
  data = data[order(data$millisSinceEpoch),]
  if (nrow(data) >= 36) {
    data.regression = make.regressable(data, n)
    model = lm(data.regression$price ~ poly(data.regression$millisSinceEpoch, degree))
    data.predicted = data.frame(fit = predict(model, newdata = data.regression)) %>%
      mutate(fit = if_else(fit < 0, 0, fit))
    for (level in levels) {
      l = substr(format(level, nsmall = 2), 3, 4)
      ci = data.frame(predict(
        model,
        newdata = data.regression,
        interval = type,
        level = level
      )) %>%
        mutate(upr = if_else(upr < 0, 0, upr)) %>%
        mutate(lwr = if_else(lwr < 0, 0, lwr)) %>%
        select(lwr, upr) %>%
        rename(!!paste0("upr", l, sep = "") := upr) %>%
        rename(!!paste0("lwr", l, sep = "") := lwr)
      data.predicted = cbind(data.predicted, ci)
    }
    return(bind_cols(data.regression, data.predicted))
  } else {
    return(NULL)
  }
}


# Compute all predictions and store in a csv
#   data:   dataset that should be expanded with predictions
#   levels: array of confidence levels for predictions
#   degree: degree of the polynome for the regression
#   n:      number of predictions
#   type:   type of interval = "confidence" or "prediction"
predict.all = function(data, levels, degree, n, type = "confidence") {
  data.predicted = data.frame()
  for (p in unique(data$product)) {
    data.product = data %>%
      filter(product == p)
    prediction = predict.product(data.product, levels, degree, n, type)
    if (!is.null(prediction)) {
      data.predicted = bind_rows(data.predicted, prediction)
    }
  }
  return(data.predicted)
}
data.prediction = predict.all(data, c(seq(0.50, 0.95, 0.05), 0.99), 3, 60, "prediction")
save.csv(data.prediction, "Datasets/food_dataset_predictions.csv")
save.json(data.prediction, "Datasets/food_dataset_predictions.json")

# Save product names
products = data.frame(product = unique(data.prediction$product))
save.csv(products, "Datasets/products.csv")
save.json(products, "Datasets/products.json")


# Testing
product.plot = function(prod, c, deg = 3, n = 60) {
  data.prod = data %>%
    filter(product == prod & country == c)
  data.prediction = predict.country(data.prod, c(seq(0.50, 0.95, 0.05), 0.99), deg, n, type =
                                      "prediction")
  ggplot(data.prediction, aes(millisSinceEpoch, price)) +
    geom_point() +
    geom_line() +
    geom_line(aes(millisSinceEpoch, fit), colour = "blue") +
    geom_ribbon(
      aes(ymin = lwr50, ymax = upr50, x = millisSinceEpoch),
      fill = "blue",
      alpha = 0.45
    ) +
    geom_ribbon(
      aes(ymin = lwr75, ymax = upr75, x = millisSinceEpoch),
      fill = "blue",
      alpha = 0.35
    ) +
    geom_ribbon(
      aes(ymin = lwr90, ymax = upr90, x = millisSinceEpoch),
      fill = "blue",
      alpha = 0.25
    ) +
    geom_ribbon(
      aes(ymin = lwr99, ymax = upr99, x = millisSinceEpoch),
      fill = "blue",
      alpha = 0.15
    ) +
    theme_minimal()
}
product.plot("wmp", "denmark")
product.plot("butter oil", "europe")
product.plot("butter", "france", deg = 3)
product.plot("cheddar", "sweden")
product.plot("asparagus - asperges, blanches/violettes, cat i - cal. 16+",
             "netherlands")

# Counting points outside prediction interval
count.outsiders = function(d) {
  product = c()
  country = c()
  outsiders = c()
  for (p in unique(d$product)) {
    data = d %>% filter(product == p)
    for (c in unique(data$country)) {
      out = data %>% filter(country == c) %>%
        filter(price < lwr95 |
                 price > upr95)
      product = c(product, p)
      country = c(country, c)
      outsiders = c(outsiders, nrow(out))
    }
  }
  overview = data.frame("product" = product,
                        "country"  = country,
                        "outsiders" = outsiders)
  return(overview)
}
outsiders = count.outsiders(data.prediction)
outsiders = outsiders[order(outsiders$outsiders),]
table(outsiders$outsiders)
boxplot(outsiders$outsiders)
outsiders %>% filter(outsiders >= 0 & product == "butter")

compute.rmse = function(d, n) {
  product = c()
  country = c()
  rmse = c()
  for (p in unique(d$product)) {
    data = d %>% filter(product == p)
    for (c in unique(data$country)) {
      datacountry = data %>% filter(country == c)
      tail = tail(datacountry[order(datacountry$millisSinceEpoch),], n)
      if (nrow(tail) == n) {
        product = c(product, p)
        country = c(country, c)
        rmse = c(rmse, sqrt(mean((tail$price - tail$fit)^2)))
      }
    }
  }
  overview = data.frame("product" = product,
                        "country"  = country,
                        "rmse" = rmse)
  return(overview)
}
# rmse = compute.rmse(data.prediction %>% filter(!is.na(fit) & !is.na(price)), 60)
# rmse = rmse[order(rmse$rmse),]
# hist(rmse$rmse)
# rmse %>% filter(rmse > 50)


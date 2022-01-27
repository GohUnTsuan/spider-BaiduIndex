library(tidyverse)

dat <- read.csv('search_index_area.csv')

plot1 <- ggplot(data = dat)  +
  geom_line(aes(x = date, y = index, linetype = keyword)) 
plot1

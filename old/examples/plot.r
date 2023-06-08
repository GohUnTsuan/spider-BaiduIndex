library(tidyverse)

dat <- read.csv('search_index.csv')
temp <- dat %>% filter(type == 'all')

plot1 <- ggplot(data = temp)  +
  geom_point(aes(x = date, y = index, color = keyword),shape=1)+
  # geom_line(aes(x = date, y = index, color = keyword,group = 1))+
  geom_smooth(aes(x = date, y = index, color = keyword,group = keyword)) +
  theme(text=element_text(family="Kai"))
plot1


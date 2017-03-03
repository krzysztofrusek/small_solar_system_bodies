require(dplyr)
require(readr)


read_fwf('slonce.txt.txt', col_positions = fwf_positions(c(1, 23), c(18, 34), c("DateJDUT", "ObsEcLon")),skip = 33) %>%
mutate(DateJDUT=DateJDUT-DateJDUT[1]+ObsEcLon[1],
       eclonResid=ObsEcLon-360/365.25*DateJDUT,
       stopnie=360/365.25*DateJDUT)->sl



require(ggplot2)
nls(eclonResid~a+b*sin(w *DateJDUT + fi) ,data=sl,start = list(a = -1, b = 1, w = 2*pi/360,fi=pi/3))->fit

sl %>%
  mutate(predicted=predict(fit)) ->sl

#geom_abline(slope=360/365.25,color="red")
ggplot(sl) + 
  geom_line(aes(x=stopnie,y=predicted,color="predicted")) + 
  geom_line(aes(x=stopnie,y=eclonResid,color="slonce"))

summary(fit)

require(dplyr)
require(readr)

#read_delim('LC_SUM_PUB.TXT', delim=' ')->lc
read_fwf('LC_SUM_PUB.TXT', col_positions = fwf_positions(c(1, 85,119), c(8, 93,127), c("nr", "dia","period")),skip = 5)->lc


lc %>%
  filter(dia < 20 ) %>%
  filter(!is.na(nr) ) %>%
  filter(!is.na(period)) %>%
  arrange(period)->lc

lc %>%
  select(nr) %>% 
  write.table(.,"dopythona.txt",col.names=F,row.names=FALSE)

#Skladanie ----
#read_csv('o.txt',col_names = F,col_types = "iDtiidiiddddddcdddddd")->o
cspec<-cols(
  .default = col_double(),
  X1 = col_integer(),
  X2 = col_date(format = "%Y-%b-%d"),
  X3 = col_time(format = "%H:%M"),
  X15 = col_character()
)
read_csv('o.txt',col_names = F,col_types = cspec)->o

wczytane<-as.numeric(o$X1)

wystapienia<-as.data.frame(table(asteroida=wczytane)) %>%
  mutate(asteroida=as.integer(as.character(asteroida)))
wystapienia %>%
  filter(Freq == 12)->komletne

setdiff(lc$nr,komletne$asteroida)->poprawka
write.table(poprawka,"dopythona2.txt",col.names=F,row.names=FALSE)

#poprawka
read_csv('o2.txt',col_names = F,col_types = cspec)->o2

left_join(o,wystapienia,by=c("X1" = "asteroida")) %>%
  filter(Freq == 12) %>%
  select(-Freq) %>%
  rbind(o2) %>%
  left_join(lc,by=c("X1" = "nr")) %>%
  arrange(X2)->asteroidy

#!/usr/bin/env Rscript

# подгружаем библиотеки
library(data.table)
library(tidyverse)
library(biomartr)
library(httr)

# создаём функцию 
genome_finder3 <- function(file, type = "organism_name", output = "name") {
  
  # загружаем файл
  names <- 
    read_delim(file, delim = "\n", col_names = type)
  
  # запрашиваем в базы данных
  gen <- map(names %>% transpose(), is.genome.available, db = 'genbank', details = T)
  ref <- map(names %>% transpose(), is.genome.available, db = 'refseq', details = T)
  
  # приводим полученные ответы в одну таблицу
  gen1 <- map(gen[sapply(1:dim(names)[1], function(x) class(gen[[x]][[1]])!="logical")], 
              mutate, seq_rel_date = as.IDate(seq_rel_date))  %>% list_rbind()
  ref1 <- map(ref[sapply(1:dim(names)[1], function(x) class(ref[[x]][[1]])!="logical")], 
              mutate, seq_rel_date = as.IDate(seq_rel_date))  %>% list_rbind()
  
  # объединяем таблицы ответов из различных баз данных и переставляем колонки для удобства
  df <- bind_rows(gen1,ref1) %>% relocate(organism_name) %>% relocate(refseq_category, .after = 2) %>% 
    relocate(excluded_from_refseq, .after=3) %>% arrange(organism_name)
  
  # получаем таблицу ненайденных запросов в случае, когда нет ответа ни от одной базы данных
  missing <- names %>% 
    slice(which(sapply(1:dim(names)[1], function(x) (class(gen[[x]][[1]])=="logical") & class(ref[[x]][[1]])=="logical")))
  
  # для ненайденных запросов taxid делаем запросы хоть на какую-то информацию
  if (type=="taxid") { # scientific name by taxid
    missing <- apply(missing, 1, function(x) content(GET(paste0('https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id/', x)))) %>%
      rbindlist(fill = T)
  }
  
  # создаём таблицу ненайденных запросов
  write_csv(missing, paste0(output, '_missing_', type, '.csv'))
  
  # создаём таблицу найденных запросов
  write_csv(df, paste0(output, "_", type, '.csv'))
}

genome_finder3(commandArgs(TRUE)[1], commandArgs(TRUE)[2], commandArgs(TRUE)[3])


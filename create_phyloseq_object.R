#!/usr/bin/R

create_pyloseq_object <- function(matrix_count, silva_tax, meta){
  
  library(vegan)
  library(phyloseq)
  library(ape)
  
  count <- read.table(matrix_count, header = TRUE)
  count = count[order(count$samples),]
  count = as.data.frame(t(count[,-1]))
  count = count[order(row.names(count)),]
  
  silva_tax = read.table(silva_tax, sep = ";", fill = TRUE)
  silva_tax_names = c("med_OTU","Domain", "Phylum","Class","Order","Family","Genus","Species","Subsp")
  silva_tax = as.matrix(silva_tax)
  silva_tax = silva_tax[-1,]
  colnames(silva_tax) = c(silva_tax_names)
  rownames(silva_tax) = c(row.names(count))
  silva_phylo_tax = tax_table(silva_tax)
  
  meta_dat = read.table(meta,sep = '\t', header = TRUE)
  meta_dat = meta_dat[order(meta_dat$sample),]
  meta_dat_ps = sample_data(meta_dat)
  colnames(count) = sample_names(meta_dat_ps)

  count_otu = otu_table(as.matrix(count), taxa_are_rows = TRUE)
  count_table_tree = as.phylo(hclust(vegdist(count, method = "bray"), "ward"))
  med_ps = phyloseq(count_otu, meta_dat_ps, count_table_tree, silva_phylo_tax)
  return(med_ps)
  }

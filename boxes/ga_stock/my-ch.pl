#!/usr/bin/perl
# proced .cdt file to choose genes
# use strict;
# use warnings;
# written on 08.01.16

my $file_cdt=$ARGV[0];	# input filename
my $sick=$ARGV[1];		# column
my $n=$ARGV[2];			# how many group do you want to choose ...row


my @total =();
my @gene_before =();

my $genes=0;
my @up_eucdis =();
my @sort_eucdis =();
my @last_genes =();
my @want_genes =();

my $i,$j,$k,$m;

open (F_cdt, "$file_cdt")||die "can't open .cdt";
open (F_gtrain, ">StockForm.txt") ||die "can't open to write";
open (F_want, ">want_stockgroup.txt") ||die "can't open to write";

## euclidean distance between gene and up gene ##
@total=<F_cdt>;
for($i=2;$i<@total;$i++)
{
	my @gene_exp =();
	$genes++;

	my @temp =();
	my $eucdis =0;
	@temp=split(/\t/,$total[$i]);

	for($j=4;$j<$sick+4;$j++)
	{
		$gene_exp[$j-4] = $temp[$j];
	}
	if($i==2)
	{
		for($m=0;$m<$sick;$m++)
		{
			$gene_before[$m] = $gene_exp[$m];
		}
		next;
	}
	else
	{
		for($k=0;$k<$sick;$k++)
		{
			$eucdis = $eucdis + (($gene_exp[$k]-$gene_before[$k])**2);
		}
		$up_eucdis[$i-3] = $eucdis;
		@gene_before = @gene_exp;
	}
}
##

## sort ##
#$genes=$genes-2;
@sort_eucdis =@up_eucdis;
for($i=0;$i<$genes-1;$i++)
{
	my $temp;
	for($j=0;$j<$genes-1;$j++)
	{
		if ($sort_eucdis[$i]>$sort_eucdis[$j])
		{
			$temp=$sort_eucdis[$i];
			$sort_eucdis[$i]=$sort_eucdis[$j];
			$sort_eucdis[$j]=$temp;
		}
	}
}
##

my $start =0;
my $point =0;		# end point
my $count =0;		# gloup gene's count

my @mid_exp=();

## gene cluster from one gene
push @last_genes,$total[0];

for($i=2;$i<@total;$i++)
{
	my @temp =();
	@temp=split(/\t/,$total[$i]);
	$point++;
	if($up_eucdis[$point-1] < $sort_eucdis[$n-1]) # $sort_eucdis[$n-2]
	{
		$count++;

		if($i==2)
		{$start =1;}

		#if($point == $genes)
		#{
			my $temp_gene;
			for($m=$start;$m<=$point;$m++)
			{
				$temp_gene = $total[$m+2];
			}
			push @last_genes,$temp_gene;
			my @temp_temp=split(/\t/,$temp_gene);
			push @want_genes,$temp_temp[1]."\n";
			##
		#}
	}
	elsif($up_eucdis[$point-1] >= $sort_eucdis[$n-1])# $sort_eucdis[$n-2]
	{
		my $temp_gene;
		for($m=$start;$m<=$point;$m++)
		{
			$temp_gene = $total[$m+2];
		}
		push @last_genes,"-----\n";
		push @want_genes,"-----\n";
		push @last_genes,$temp_gene;
		my @temp_temp=split(/\t/,$temp_gene);
		push @want_genes,$temp_temp[1]."\n";

		##
		$start = $point+1;
	}
}
print F_gtrain @last_genes;
print F_want @want_genes;

close F_cdt;
close F_gtrain;
close F_want;
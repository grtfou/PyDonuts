#!/usr/bin/perl
# take to test file want gene's data
# use strict;
# use warnings;
# written on 07.12.21

#my $file_input = 'in_count.txt';

my $i,$j,$k,$m;

my $file_input=$ARGV[0]; #input的檔名
my $out_name=$ARGV[1];  #output的檔名
my $Appear_time=$ARGV[2];

open (F_input, "$file_input")||die "can't open file_input.txt";
open (F_ouput, ">$out_name") ||die "can't open to write";

my @stock = <F_input>;
my @stock_output = ();

for($i=0;$i<@stock;$i++)			# 算stock出現幾次
{
	my $count =0;
	my @temp = split(/ /,$stock[$i]);
	$name=$temp[0];

	for($j=0;$j<@stock;$j++)
	{
		my @temp2 = split(/ /,$stock[$j]);
		if($temp[0] eq $temp2[0])
		{
			$count++;
		}
	}
	push @stock_output,$count." ".$name."\n";
}

for($k=0;$k<@stock_output;$k++)			# 去除已經算過卻重覆出現的stock
{
	for($m=$k+1;$m<@stock_output;$m++)
	{
		if($stock_output[$k] eq $stock_output[$m])
		{
			$stock_output[$k]='';
		}
	}
}
#print F_ouput @stock_output;

for($i=0;$i<@stock_output;$i++)			# 挑出一年有出現$Appear_time次以上的stock
{
	my @temp = split(/ /,$stock_output[$i]);
	if ($temp[0] >= $Appear_time)
	{
		$stock_NameList[$i]=$temp[1];
	}
}

print F_ouput @stock_NameList;


close F_input;
close F_ouput;
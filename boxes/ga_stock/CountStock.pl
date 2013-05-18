#!/usr/bin/perl
# take to test file want gene's data
# use strict;
# use warnings;
# written on 07.12.21

#my $file_input = 'in_count.txt';

my $i,$j,$k,$m;

my $file_input=$ARGV[0]; #input���ɦW
my $out_name=$ARGV[1];  #output���ɦW
my $Appear_time=$ARGV[2];

open (F_input, "$file_input")||die "can't open file_input.txt";
open (F_ouput, ">$out_name") ||die "can't open to write";

my @stock = <F_input>;
my @stock_output = ();

for($i=0;$i<@stock;$i++)			# ��stock�X�{�X��
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

for($k=0;$k<@stock_output;$k++)			# �h���w�g��L�o���ХX�{��stock
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

for($i=0;$i<@stock_output;$i++)			# �D�X�@�~���X�{$Appear_time���H�W��stock
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
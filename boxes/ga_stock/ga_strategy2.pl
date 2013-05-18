#!/usr/bin/perl
#############################
# GA paper   by cychen  08.02.15
# 輸入資料:股名,報酬,風險
# fitness function = Sharp Ratio = 報酬 / 風險
#############################
# use strict;
# use warnings;

#股票資訊的檔名
chomp(my $file_stock_inf=$ARGV[0]);
open (F_stock_inf, "$file_stock_inf")||die "can't open stock's information file\n";
my @stock_inf_total=<F_stock_inf>;

#想要產生多少數量的染色體
chomp(my $chromosome_count = $ARGV[1]);				#染色體數(股票資金分配的策略個數)
#交配率(crossover rate)[輸入0~1之間的數字]:
chomp(my $crossover_rate = $ARGV[2]);				#交配率(每條染色體多少機率會被交配)
#突變率(crossover rate)[輸入0~1之間的數字]:
chomp(my $mutation_rate = $ARGV[3]);				#突變率(總基因數有多少比例會被突變)
#最大疊代次數(停止條件):
chomp(my $run_time = $ARGV[4]);						#如果都不能收儉，最多跑幾次
#print "世代收儉差異度(停止條件)[輸入0~1之間的數字]:";
#chomp(my $difference_rang = <STDIN>);						#如果收儉，是本代比上一代差異差在多少之間

###########################全域變數區########################################
### 收集染色體的平均報酬及風險 ###
	my @sharpRatio=();
### 產生chromosome ###
	my $gene_count=$#stock_inf_total; #每條染色體中的基因(股票)數
	my @chromosome_cluster=();
### 進行適應函數的運算 ###
	my @fitnessFunction=();
	my $chromosome_num=0;			#當chromosome_cluster的計數
### 排序(排名次) ###
	my @temp_fitnessFunction=();	#暫存fitnessFunction排序後結果
	my $fitnessFunction_vs=0;
	my @last_chromosome=();
	my @over_cross=();				#交配完後的染色體
	my @over_mutation=();			#突變完後的染色體
	my @over_normalization=();		#正規化完的染色體
	my @OldNice_chromosome=();		#前一代最佳的染色體
	my @ThisNice_chromosome=();		#本代交配突變完的染色體
	my @TheNew_chromosome=();		#新一代染色體

##########################################################################
for(my $now_runTime=0;$now_runTime<$run_time;++$now_runTime)
{
#$file_write="nice_answer$now_runTime.txt";
#open (F_output, ">$file_write") || die "can't output answer file\n";
	if($now_runTime==0)
	{
		cal_chromo_AvgCash_Risk();	### 收集染色體的平均報酬及風險 ### in:輸入檔; out:@sharpRatio
		create_chromosome();		###產生新的染色體 ### out:@chromosome_cluster
	}
	cal_fitness_function(@chromosome_cluster);		### 進行適應函數的運算 ### in:染色體群; out:@fitnessFunction
	sort_fitness_function(10,@fitnessFunction);		### 排序(排名次) ，第一格參數代表要選前百分之幾 ### in:@fitnessFunction; out:$fitnessFunction_vs
	@OldNice_chromosome=Selection();				### 上上一代最好的精英 ### in:@chromosome_cluster,$fitnessFunction_vs

	#print "-------------------↑交配前------------------------\n";
	@last_chromosome=@chromosome_cluster;
	@over_cross=crossover();						### in:@last_chromosome
	@over_generation=mutation();					### in:@over_cross
	#@over_normalization=normalization(@over_mutation);
	#print "-------------------↓世代結束--------------------\n";
	#print @over_normalization;
	#@over_generation=@over_normalization;

	@fitnessFunction=();
	$fitnessFunction_vs=0;
	@chromosome_cluster=@over_generation;
	cal_fitness_function(@over_generation);			### 進行適應函數的運算 ### in:染色體群; out:@fitnessFunction
	sort_fitness_function(90,@fitnessFunction);		### 排序(排名次) ，第一格參數代表要選前百分之幾 ### in:@fitnessFunction; out:$fitnessFunction_vs
	@ThisNice_chromosome=Selection();				### 交配突變後本代最好的精英 ### in:@chromosome_cluster,$fitnessFunction_vs

	@TheNew_chromosome=();
	push @TheNew_chromosome,@OldNice_chromosome;
	push @TheNew_chromosome,@ThisNice_chromosome;
	@TheNew_chromosome=normalization(@TheNew_chromosome);

	@fitnessFunction=();
	$fitnessFunction_vs=0;
	#@chromosome_cluster=@over_generation;
	@chromosome_cluster=@TheNew_chromosome;
	cal_fitness_function(@TheNew_chromosome);		### 進行適應函數的運算  ### in:染色體群; out:@fitnessFunction
	sort_fitness_function(100,@fitnessFunction);	### 排序(排名次) ，第一格參數代表要選前百分之幾 ### in:@fitnessFunction; out:$fitnessFunction_vs
	@TheNew_chromosome=Selection();					### 本代染色體 ### in:@chromosome_cluster,$fitnessFunction_vs

	### 找出最佳的適應函數為多少 ###
	my @this_temp_fitnessFunction=@fitnessFunction;	#暫存fitnessFunction排序後結果
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		for(my $j=0;$j<$chromosome_count;++$j)
		{
			if($this_temp_fitnessFunction[$i]>$this_temp_fitnessFunction[$j])
			{
				my $temp=0;
				$temp=$this_temp_fitnessFunction[$i];
				$this_temp_fitnessFunction[$i]=$this_temp_fitnessFunction[$j];
				$this_temp_fitnessFunction[$j]=$temp;
			}
		}
	}
	##**end 找出最佳的適應函數為多少 ###

	my $temp_runTime=$now_runTime+1;
	print "\n 第$temp_runTime世代的_第一名適應函數 $this_temp_fitnessFunction[0]";
	print "==============本世代結束====================\n";

	##印出基金分配的組合
	if($now_runTime==$run_time-1)
	{
		$file_write="Generation $run_time.txt";
		open (F_output, ">$file_write") || die "can't output answer file\n";

		my $temp_num=0;
		for(my $f=0;$f<$chromosome_count;++$f)
		{
			for(my $g=0;$g<$gene_count;++$g)
			{
				print F_output $TheNew_chromosome[$temp_num]."\t";
				++$temp_num;
			}
			print F_output "$fitnessFunction[$f]";

			### 印出最佳的染色體 ###
			if ($this_temp_fitnessFunction[0]==$fitnessFunction[$f])
			{
				my $file_niceout="$ARGV[1]染色體_$ARGV[2]交配率_$ARGV[3]突變率_$ARGV[4]世代次數.txt";
				open (F_outnice, ">$file_niceout") || die "can't output answer file\n";

				for(my $h=0;$h<$gene_count;++$h)
				{
					#print $TheNew_chromosome[$f*$gene_count+$h]."\t";
					print F_outnice $TheNew_chromosome[$f*$gene_count+$h]."\t";
				}
			}
			close (F_outnice);
			##**end 印出最佳的染色體 ###
		}
		close(F_output);
	}
	@fitnessFunction=();
	@chromosome_cluster=@TheNew_chromosome;
}
close(F_stock_inf);


### 收集染色體的平均報酬及風險 ###
sub cal_chromo_AvgCash_Risk()
{
	my $ave_increment=0;	#平均報酬
	my $risk=0;			#風險
	my $sharp_ratio=0; 	#適應函數，採用sharp比率
	@sharpRatio=();
	for(my $i=1;$i<@stock_inf_total;++$i)
	{
		my @temp=();
		@temp=split(/\t/,$stock_inf_total[$i]);
		for(my $j=1;$j<@temp;++$j)
		{
			if($j<=@temp-2)
			{
				$ave_increment+=$temp[$j];
			}
			elsif ($j==@temp-1)
			{
				$risk=$temp[$j];
			}
		}
		$ave_increment/=(@temp-2);
		#print $ave_increment."\n";
		#print $risk."\n";

		$sharp_ratio=$ave_increment/$risk;
		push @sharpRatio,$sharp_ratio;

		$ave_increment=0;
		$risk=0;
	}
}
##**end 收集染色體的平均報酬及風險 ###

### 產生chromosome ###
sub create_chromosome
{
	@chromosome_cluster=();
	for(my $count1=1;$count1<=$chromosome_count;$count1++)
	{
		my @chromosome =();
		my $gene=0;
		for(my $i=1;$i<=$gene_count;++$i)
		{
			$gene = sprintf "%.3f", rand(1);#$cash_ratio_surplus); #資金分配的比率亂數決定，取到小數第三位
			push @chromosome,$gene;
		}
		push @chromosome_cluster,@chromosome;
		#print @chromosome;
		#print "\n";
	}
}
##**end 產生chromosome ###

### 進行適應函數的運算 ###
sub cal_fitness_function
{
	my (@cal_temp_chromosome)=@_;
	@fitnessFunction=();
	$chromosome_num=0;	#當chromosome_cluster的計數
	for(my $count2=1;$count2<=$chromosome_count;$count2++)
	{
		my $fitness_function=0;
		for(my $i=0;$i<$gene_count;++$i)
		{
			my $one_stock_fit=0;
			$one_stock_fit=$cal_temp_chromosome[$chromosome_num]*$sharpRatio[$i];
			$fitness_function+=$one_stock_fit;
			#print $one_stock_fit,"\n";
			#print $chromosome_num,$i,"\n";
			++$chromosome_num;
		}
		push @fitnessFunction,$fitness_function."\n";
	}
	#print @fitnessFunction;
	#print "\n";
}
##**end 進行適應函數的運算 ###

### 排序(排名次) ###
sub sort_fitness_function
{
	my ($wantRate,@wantToSort)=@_;		# 想要排序的fitness_function陣列
	$fitnessFunction_vs=0;
	@temp_fitnessFunction=@wantToSort;	#暫存fitnessFunction排序後結果
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		for(my $j=0;$j<$chromosome_count;++$j)
		{
			if($temp_fitnessFunction[$i]>$temp_fitnessFunction[$j])
			{
				my $temp=0;
				$temp=$temp_fitnessFunction[$i];
				$temp_fitnessFunction[$i]=$temp_fitnessFunction[$j];
				$temp_fitnessFunction[$j]=$temp;
			}
		}
	}
	#fintnessFunction 前百分之多少 與 後百分之多少的那個區隔數字(百分之50的話，就是指中位數)
	$fitnessFunction_vs=$temp_fitnessFunction[int(($chromosome_count*$wantRate/100)-1)];
	#print @fitnessFunction;
	#print @temp_fitnessFunction;
	#print "\n";
	#print $fitnessFunction_vs;
}
##**end 排序(排名次) ###

############################################
### 選擇 ###
sub Selection
{
	my @temp_new_chromosome=();
	$chromosome_num=0;
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		if($fitnessFunction[$i]>=$fitnessFunction_vs)
		{
			for(my $j=0;$j<$gene_count;++$j)
			{
				push @temp_new_chromosome,$chromosome_cluster[$chromosome_num];
				#print $chromosome_cluster[$chromosome_num]."\n";
				++$chromosome_num;
			}
		}
		else
		{
			$chromosome_num=$chromosome_num+$gene_count;
		}
		#print "\n";
	}
	return @temp_new_chromosome;
}
##**end 選擇 ###

## 複製：本代=前一代+這一代，如果是第一代，就本代=第一代+第一代 ###
sub CopyChromosome
{
	my (@get_addChromosome)=@_;
	my @temp_copy_chromosome=@get_addChromosome;
	for (my $i=0;$i<@get_addChromosome;++$i)
	{
		push @temp_copy_chromosome,$get_addChromosome[$i];
	}
	return @temp_copy_chromosome;
}
##**end 複製 ###

### 交配：雙點交配 ###
sub crossover
{
	### 將配對的染色體次序打亂########
	my @tempSeed1=();
	my @tempSeed2=();

	for(my $i=0;$i<$chromosome_count;++$i)
	{
		my $temp_ran=int (rand 2);
		if($temp_ran==0 && ($#tempSeed1+$#tempSeed2+1)<=$chromosome_count-1)
		{
			push @tempSeed1,$i;
		}
		elsif($temp_ran==1 && ($#tempSeed1+$#tempSeed2+1)<=$chromosome_count-1)
		{
			push @tempSeed2,$i;
		}
		else	#例外處理
		{
			print "XXXXXXXXXXXXXXXXXXXXXX $temp_ran XXXXXXXXXXXXXXXXX\n";
		}
	}
	push @RandSeed,@tempSeed1;
	push @RandSeed,@tempSeed2;

	#print @RandSeed;

	##########################

	my @crossover_chromosome1=();
	my @crossover_chromosome2=();
	my $crossRate=$crossover_rate;

	for(my $i=0;$i<$chromosome_count;$i=$i+2)
	{
		#如果丟出來的rand數比突變率大，那麼就不進行交配，直接將染色體輸出到下一代
		my $this_chromosome_rand = rand(1);

		if ($this_chromosome_rand >$crossRate)
		{
			for(my $g=0;$g<$gene_count;++$g)
			{
				push @crossover_chromosome1,$last_chromosome[($gene_count*$RandSeed[$i])+$g];
				push @crossover_chromosome2,$last_chromosome[($gene_count*$RandSeed[$i+1])+$g];
				#print $last_chromosome[$gene_count*$RandSeed[$i]+$g]."\t";
				#print $last_chromosome[$gene_count*$RandSeed[$i+1]+$g]."\t";
				#print "\n";
			}
		}
		else
		{
			my $first_point=int(rand($gene_count)); #雙點交配的第一個點，會產生0~小於基因數的亂數
			my $second_point=int(rand($gene_count-$first_point))+$first_point; #雙點交配的第二個點，會產生0~小於first_point的亂數
			#$chromosome_num=0;

			for(my $j=0;$j<$gene_count;++$j)
			{
				if($j>=$first_point && $j<=$second_point)	#位於雙點之內，就push 別人基因，否則就push 自已基因
				{
					#$gene_count*$RandSeed[] 代表起始位置，+$chromosome_num 代表該染色體的第幾個基因
					push @crossover_chromosome1,$last_chromosome[$gene_count*$RandSeed[$i+1]+$j];
					push @crossover_chromosome2,$last_chromosome[$gene_count*$RandSeed[$i]+$j];
					#print $last_chromosome[$gene_count*$RandSeed[$i+1]+$chromosome_num]."\t";
					#print $last_chromosome[$gene_count*$RandSeed[$i]+$chromosome_num]."\t";
				}
				else	#印第一條(自己)
				{
					push @crossover_chromosome1,$last_chromosome[$gene_count*$RandSeed[$i]+$j];
					push @crossover_chromosome2,$last_chromosome[$gene_count*$RandSeed[$i+1]+$j];
					#print $last_chromosome[$gene_count*$RandSeed[$i]+$chromosome_num]."\t";
					#print $last_chromosome[$gene_count*$RandSeed[$i+1]+$chromosome_num]."\t";
				}
				#++$chromosome_num;
			}
			#print "$first_point  $second_point\n";
		}
	}
	@RandSeed=();
	my @AllCrossoverChromosome=();
	push @AllCrossoverChromosome,@crossover_chromosome1;
	push @AllCrossoverChromosome,@crossover_chromosome2;
	return @AllCrossoverChromosome;
}
##**end 交配 ###

### 突變 ###
sub mutation()
{
	my $AllGeneCount = $gene_count* $chromosome_count; 	#總基因數
	my $TheMutationRate=$mutation_rate; 				#設定的突變率
	my $WantTo_MutationCount =$AllGeneCount*$TheMutationRate;
	my @temp_mut=@over_cross;
	$WantTo_MutationCount=int($WantTo_MutationCount+0.5);#四捨五入

	#若總基因數*突變率 小於 1的話，就0.9的機率進行突變1個基因，0.1的機率不進行突變
	if ($WantTo_MutationCount <=0)
	{
		if(rand(1)>0.9)
		{
			$WantTo_MutationCount=1;
		}
	}
	for($i=1;$i<=$WantTo_MutationCount;++$i)
	{
		my $chang_MatrixPosition= int(rand($AllGeneCount));
		$temp_mut[$chang_MatrixPosition]= sprintf "%.3f", rand(1);

		#print "XX$temp_mut[$chang_MatrixPosition].X$chang_MatrixPosition\n";
	}
	return @temp_mut;
}
##**end 突變 ###

###正規化：使投資比例加起來為100% (即為1) ###
sub normalization()
{
	my @temp_norm=@_;
	for(my $i=0;$i<$chromosome_count;++$i)
	{
		my $one_chromAll=0;
		for(my $j=0;$j<$gene_count;++$j)
		{
			$one_chromAll+=$temp_norm[$i*$gene_count+$j];
		}
		for(my $k=0;$k<$gene_count;++$k)
		{
			if($one_chromAll==0)	#例外處理
			{
			   print "=====================分母為0=====================";
			}
			$temp_norm[$i*$gene_count+$k] /= $one_chromAll;
			$temp_norm[$i*$gene_count+$k]= sprintf "%.3f",$temp_norm[$i*$gene_count+$k];
		}
		#my $gg=0;
		#for(my $m=0;$m<$gene_count;++$m)
		#{
		#	$gg+=$temp_norm[$i*$gene_count+$m];
		#}
		#print "$gg\n";
	}
	return @temp_norm;
}
##**正規化###


teste = cdrsReport.objects.using('sippulse_reports').filter(created__range=dr, provider_name__in=['LIGUE TELECOM', 'LIGUE TELECOM 3/30/6', 'LIGUE_FIX_ROC', 'LIGUE_INTER_0/60/60']).values('provider_name', 'callee_id', 'call_start_time', 'duration', 'duration_block')

https://adm.otimatel.com.br/media/cdr/reports/ligue-novo.csv

https://adm.otimatel.com.br/media/cdr/reports/contrato_movile.pdf
https://adm.otimatel.com.br/media/cdr/reports/contrato_movile1.pdf
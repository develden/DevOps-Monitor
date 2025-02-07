from django.db.models import F, ExpressionWrapper, DurationField, Avg
from datetime import timedelta
from .models import Build
import numpy as np

def analyze_build_times():
    """
    Анализ времени сборок.
    Вычисляется среднее время сборки и количество сборок, длительность которых превышает заданный порог.
    Порог здесь задан в секундах (например, 300 секунд = 5 минут).
    """
    builds_with_duration = Build.objects.exclude(started_at__isnull=True).exclude(finished_at__isnull=True).annotate(
        duration=ExpressionWrapper(F('finished_at') - F('started_at'), output_field=DurationField())
    )
    average_duration = builds_with_duration.aggregate(avg_duration=Avg('duration'))['avg_duration']
    threshold_seconds = 300
    builds_above_threshold = builds_with_duration.filter(duration__gt=timedelta(seconds=threshold_seconds)).count()
    total_builds = Build.objects.count()
    
    analysis = {
        'average_build_time': average_duration,
        'builds_above_threshold': builds_above_threshold,
        'total_builds': total_builds
    }
    return analysis

def analyze_failures():
    """
    Анализ неудачных сборок.
    Вычисляется процент сборок со статусом 'failed'.
    """
    total_builds = Build.objects.count()
    failed_builds = Build.objects.filter(status='failed').count()
    failure_rate = (failed_builds / total_builds * 100) if total_builds > 0 else 0

    analysis = {
        'failed_builds': failed_builds,
        'total_builds': total_builds,
        'failure_rate': failure_rate,
    }
    return analysis

def analyze_builds():
    """
    Объединённый метод анализа сборок.
    Возвращает как информацию о времени сборок, так и данные по неудачным сборкам.
    Эти данные могут использоваться для визуализации аналитики на дашборде.
    """
    build_time_analysis = analyze_build_times()
    failure_analysis = analyze_failures()
    trend_analysis = analyze_trend()

    analysis = {**build_time_analysis, **failure_analysis, **trend_analysis}
    return analysis

def analyze_trend():
    """
    Анализ тенденции времени сборок на основе последних N сборок.
    Используется простая линейная регрессия для вычисления наклона (тренда).
    Если наклон положительный — время сборок растёт, отрицательный — уменьшается.
    """
    recent_builds = Build.objects.exclude(started_at__isnull=True).exclude(finished_at__isnull=True).order_by('-finished_at')[:10]
    if recent_builds.count() < 2:
        return {'trend': 'Недостаточно данных для анализа', 'slope': None}

    durations = [ (build.finished_at - build.started_at).total_seconds() for build in recent_builds ]
    x = np.arange(len(durations))
    y = np.array(durations)
    slope, intercept = np.polyfit(x, y, 1)
    trend = 'увеличивается' if slope > 0 else 'уменьшается' if slope < 0 else 'стабильно'
    return {'trend': trend, 'slope': slope, 'moving_average': float(np.mean(durations))} 
"""
Risk Analysis Module
Calculates seismic risk assessments with confidence scores and trends
"""

from typing import List, Dict
from datetime import datetime, timedelta
import math


class RiskAnalyzer:
    """
    Analyzes seismic data to produce risk assessments
    """

    # Critical fault segments with historical context
    CRITICAL_SEGMENTS = {
        'Istanbul': {
            'fault': 'North Anatolian Fault - Marmara Segment',
            'last_major_event_year': 1766,
            'recurrence_interval_years': 250,
            'baseline_risk': 'HIGH',
            'context': 'Princes Islands segment - 259-year seismic gap'
        },
        'Marmara': {
            'fault': 'North Anatolian Fault - Marmara Sea',
            'last_major_event_year': 1912,
            'recurrence_interval_years': 200,
            'baseline_risk': 'HIGH',
            'context': 'Critical seismic gap beneath Marmara Sea'
        },
        'Aegean': {
            'fault': 'Aegean extensional zone',
            'last_major_event_year': 2020,
            'recurrence_interval_years': 50,
            'baseline_risk': 'MEDIUM',
            'context': 'Active seismic zone with frequent moderate events'
        },
        'Eastern_Anatolia': {
            'fault': 'East Anatolian Fault',
            'last_major_event_year': 2023,
            'recurrence_interval_years': 100,
            'baseline_risk': 'MEDIUM',
            'context': 'Recent major events (Feb 2023 M7.8 and M7.5)'
        }
    }

    def __init__(self):
        pass

    def calculate_risk_assessment(self, region: str, events: List[Dict]) -> Dict:
        """
        Calculate comprehensive risk assessment for a region

        Args:
            region: Region name
            events: List of recent earthquake events

        Returns:
            Risk assessment dictionary
        """
        if region not in self.CRITICAL_SEGMENTS:
            region = 'Other'

        # Get baseline risk
        segment_info = self.CRITICAL_SEGMENTS.get(region, {
            'fault': 'Unknown',
            'baseline_risk': 'LOW',
            'context': 'No critical fault identified'
        })

        # Calculate components
        event_rate_score = self._calculate_event_rate_score(events)
        magnitude_score = self._calculate_magnitude_score(events)
        pattern_score = self._calculate_pattern_score(events)
        temporal_score = self._calculate_temporal_score(events)

        # Combine scores
        combined_score = (
            event_rate_score * 0.3 +
            magnitude_score * 0.3 +
            pattern_score * 0.2 +
            temporal_score * 0.2
        )

        # Determine risk level
        base_risk = segment_info['baseline_risk']
        risk_level = self._determine_risk_level(base_risk, combined_score)

        # Calculate probabilities
        probabilities = self._calculate_probabilities(region, events, combined_score)

        # Calculate confidence
        confidence = self._calculate_confidence(events, combined_score)

        # Determine trend
        trend = self._calculate_trend(events)

        # Generate contributing factors
        contributing_factors = self._generate_contributing_factors(
            region, events, event_rate_score, magnitude_score, pattern_score
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(region, risk_level, events)

        return {
            'region': region,
            'risk_level': risk_level,
            'probability_m5_7days': probabilities['m5_7days'],
            'probability_m6_30days': probabilities['m6_30days'],
            'confidence': confidence,
            'trend': trend,
            'contributing_factors': contributing_factors,
            'recommendations': recommendations,
            'fault_context': segment_info['context'],
            'event_count_analyzed': len(events),
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _calculate_event_rate_score(self, events: List[Dict]) -> float:
        """
        Score based on event rate (0-100)
        """
        if not events:
            return 0.0

        # Events per day
        if len(events) == 0:
            return 0.0

        time_span_days = max(1, (
            max(e['datetime_obj'] for e in events) -
            min(e['datetime_obj'] for e in events)
        ).days)

        events_per_day = len(events) / time_span_days

        # Score: 0-2 events/day = 0-30, 2-5 = 30-60, 5+ = 60-100
        if events_per_day < 2:
            score = events_per_day * 15
        elif events_per_day < 5:
            score = 30 + (events_per_day - 2) * 10
        else:
            score = min(100, 60 + (events_per_day - 5) * 8)

        return score

    def _calculate_magnitude_score(self, events: List[Dict]) -> float:
        """
        Score based on recent magnitudes (0-100)
        """
        if not events:
            return 0.0

        max_mag = max(e['magnitude'] for e in events)

        # Score based on maximum magnitude
        if max_mag < 3.0:
            score = 20
        elif max_mag < 4.0:
            score = 40
        elif max_mag < 5.0:
            score = 70
        elif max_mag < 6.0:
            score = 90
        else:
            score = 100

        # Boost if multiple significant events
        significant_count = len([e for e in events if e['magnitude'] >= 4.0])
        if significant_count >= 2:
            score = min(100, score + significant_count * 5)

        return score

    def _calculate_pattern_score(self, events: List[Dict]) -> float:
        """
        Score based on detected patterns (0-100)
        """
        if len(events) < 3:
            return 10.0

        score = 20.0  # baseline

        # Check for clustering
        cluster_score = self._detect_clustering_score(events)
        score += cluster_score * 0.4

        # Check for increasing rate
        rate_increase_score = self._detect_rate_increase(events)
        score += rate_increase_score * 0.6

        return min(100, score)

    def _detect_clustering_score(self, events: List[Dict]) -> float:
        """
        Detect spatial clustering (0-100)
        """
        if len(events) < 3:
            return 0.0

        # Calculate average inter-event distance
        distances = []
        for i in range(len(events) - 1):
            for j in range(i + 1, len(events)):
                dist = self._haversine_distance(
                    events[i]['latitude'], events[i]['longitude'],
                    events[j]['latitude'], events[j]['longitude']
                )
                distances.append(dist)

        if not distances:
            return 0.0

        avg_distance = sum(distances) / len(distances)

        # Closer clustering = higher score
        if avg_distance < 10:
            return 80
        elif avg_distance < 30:
            return 50
        elif avg_distance < 50:
            return 30
        else:
            return 10

    def _detect_rate_increase(self, events: List[Dict]) -> float:
        """
        Detect if event rate is increasing (0-100)
        """
        if len(events) < 6:
            return 20.0

        # Sort by time
        sorted_events = sorted(events, key=lambda x: x['datetime_obj'])

        # Split into first half and second half
        mid_point = len(sorted_events) // 2
        first_half = sorted_events[:mid_point]
        second_half = sorted_events[mid_point:]

        # Calculate rates
        first_duration = (first_half[-1]['datetime_obj'] - first_half[0]['datetime_obj']).total_seconds() / 86400
        second_duration = (second_half[-1]['datetime_obj'] - second_half[0]['datetime_obj']).total_seconds() / 86400

        if first_duration == 0 or second_duration == 0:
            return 20.0

        first_rate = len(first_half) / max(1, first_duration)
        second_rate = len(second_half) / max(1, second_duration)

        # Calculate increase ratio
        if first_rate == 0:
            return 50.0

        rate_ratio = second_rate / first_rate

        # Score based on increase
        if rate_ratio > 2.0:
            return 90
        elif rate_ratio > 1.5:
            return 70
        elif rate_ratio > 1.2:
            return 50
        elif rate_ratio > 0.8:
            return 30
        else:
            return 10

    def _calculate_temporal_score(self, events: List[Dict]) -> float:
        """
        Score based on temporal patterns (0-100)
        """
        if len(events) < 2:
            return 20.0

        sorted_events = sorted(events, key=lambda x: x['datetime_obj'])

        # Calculate inter-event times
        inter_event_times = []
        for i in range(len(sorted_events) - 1):
            time_diff_hours = (sorted_events[i+1]['datetime_obj'] - sorted_events[i]['datetime_obj']).total_seconds() / 3600
            inter_event_times.append(time_diff_hours)

        if not inter_event_times:
            return 20.0

        # Shorter inter-event times = higher score
        avg_inter_event = sum(inter_event_times) / len(inter_event_times)

        if avg_inter_event < 1:  # < 1 hour
            return 90
        elif avg_inter_event < 6:  # < 6 hours
            return 70
        elif avg_inter_event < 24:  # < 1 day
            return 50
        else:
            return 30

    def _determine_risk_level(self, baseline: str, score: float) -> str:
        """
        Determine risk level from baseline and score
        """
        if baseline == 'HIGH':
            # Istanbul/Marmara always HIGH unless score is very low
            return 'HIGH' if score > 30 else 'MEDIUM'
        elif baseline == 'MEDIUM':
            if score > 70:
                return 'HIGH'
            elif score > 40:
                return 'MEDIUM'
            else:
                return 'LOW'
        else:
            if score > 80:
                return 'HIGH'
            elif score > 50:
                return 'MEDIUM'
            else:
                return 'LOW'

    def _calculate_probabilities(self, region: str, events: List[Dict], score: float) -> Dict:
        """
        Calculate probabilistic forecasts
        """
        # Base probabilities (simplified ETAS-like approach)
        base_p_m5_7d = 0.01
        base_p_m6_30d = 0.005

        # Adjust based on region
        if region in ['Istanbul', 'Marmara']:
            base_p_m5_7d *= 2
            base_p_m6_30d *= 3

        # Adjust based on recent activity
        if events:
            max_mag = max(e['magnitude'] for e in events)
            if max_mag >= 5.0:
                base_p_m5_7d *= 5
                base_p_m6_30d *= 3
            elif max_mag >= 4.0:
                base_p_m5_7d *= 2
                base_p_m6_30d *= 1.5

        # Adjust based on score
        score_multiplier = 1 + (score / 100)

        return {
            'm5_7days': min(0.5, base_p_m5_7d * score_multiplier),
            'm6_30days': min(0.3, base_p_m6_30d * score_multiplier)
        }

    def _calculate_confidence(self, events: List[Dict], score: float) -> int:
        """
        Calculate confidence in assessment (0-100)
        """
        confidence = 50  # baseline

        # More events = higher confidence
        event_count_factor = min(30, len(events) * 2)
        confidence += event_count_factor

        # Score extremes = higher confidence
        if score > 80 or score < 20:
            confidence += 10

        # Cap at reasonable level for short-term forecasts
        return min(85, confidence)

    def _calculate_trend(self, events: List[Dict]) -> str:
        """
        Determine if activity is increasing, stable, or decreasing
        """
        if len(events) < 6:
            return 'STABLE'

        rate_increase = self._detect_rate_increase(events)

        if rate_increase > 60:
            return 'INCREASING'
        elif rate_increase < 40:
            return 'DECREASING'
        else:
            return 'STABLE'

    def _generate_contributing_factors(
        self, region: str, events: List[Dict],
        event_rate_score: float, magnitude_score: float, pattern_score: float
    ) -> List[str]:
        """
        Generate human-readable contributing factors
        """
        factors = []

        # Regional context
        if region in self.CRITICAL_SEGMENTS:
            factors.append(self.CRITICAL_SEGMENTS[region]['context'])

        # Event rate
        if event_rate_score > 60:
            factors.append(f"Elevated seismic activity rate ({len(events)} events analyzed)")
        elif event_rate_score < 30:
            factors.append("Low background seismicity")

        # Magnitude
        if events:
            max_mag = max(e['magnitude'] for e in events)
            if max_mag >= 4.5:
                factors.append(f"Recent significant event (M{max_mag:.1f})")
            elif max_mag < 3.0:
                factors.append("No significant events detected")

        # Patterns
        if pattern_score > 60:
            factors.append("Spatial clustering detected")

        return factors

    def _generate_recommendations(self, region: str, risk_level: str, events: List[Dict]) -> List[str]:
        """
        Generate actionable recommendations
        """
        recommendations = []

        if risk_level == 'HIGH':
            recommendations.extend([
                "Maintain high-level emergency preparedness",
                "Review and update earthquake response plans",
                "Ensure emergency supply kits are stocked",
                "Verify structural integrity of critical infrastructure"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "Continue routine seismic monitoring",
                "Maintain emergency preparedness kits",
                "Review building seismic compliance"
            ])
        else:
            recommendations.extend([
                "Maintain standard preparedness measures",
                "Regular review of emergency procedures"
            ])

        # Region-specific
        if region == 'Istanbul':
            recommendations.append("Istanbul high-risk zone: ensure building codes compliance")

        return recommendations

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in km"""
        R = 6371
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

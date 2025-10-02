"""
Data Processing and Normalization Module
Handles deduplication, merging, regional classification, and pattern detection
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import math
from collections import defaultdict


class SeismicDataProcessor:
    """
    Processes and normalizes earthquake data from multiple sources
    """

    # Turkey regional boundaries
    REGIONS = {
        'Istanbul': {
            'bbox': {'lat_min': 40.8, 'lat_max': 41.3, 'lon_min': 28.5, 'lon_max': 29.5},
            'priority': 1
        },
        'Marmara': {
            'bbox': {'lat_min': 40.0, 'lat_max': 41.2, 'lon_min': 26.5, 'lon_max': 29.8},
            'priority': 2
        },
        'Aegean': {
            'bbox': {'lat_min': 37.0, 'lat_max': 40.0, 'lon_min': 26.0, 'lon_max': 29.0},
            'priority': 3
        },
        'Eastern_Anatolia': {
            'bbox': {'lat_min': 38.0, 'lat_max': 41.0, 'lon_min': 38.0, 'lon_max': 44.0},
            'priority': 4
        },
        'Central_Anatolia': {
            'bbox': {'lat_min': 38.0, 'lat_max': 41.0, 'lon_min': 32.0, 'lon_max': 38.0},
            'priority': 5
        },
        'Other': {
            'bbox': {'lat_min': 36.0, 'lat_max': 42.0, 'lon_min': 26.0, 'lon_max': 45.0},
            'priority': 99
        }
    }

    def __init__(self):
        pass

    def normalize_and_merge(self, afad_events: List[Dict], emsc_events: List[Dict]) -> List[Dict]:
        """
        Normalize events from different sources and merge duplicates

        Args:
            afad_events: Events from AFAD
            emsc_events: Events from EMSC

        Returns:
            Merged and deduplicated event list
        """
        # Normalize timestamps
        all_events = []

        for event in afad_events:
            normalized = self._normalize_event(event)
            if normalized:
                all_events.append(normalized)

        for event in emsc_events:
            normalized = self._normalize_event(event)
            if normalized:
                all_events.append(normalized)

        # Deduplicate
        merged_events = self._deduplicate_events(all_events)

        # Classify regions
        for event in merged_events:
            event['region'] = self._classify_region(event['latitude'], event['longitude'])

        return merged_events

    def _normalize_event(self, event: Dict) -> Optional[Dict]:
        """
        Normalize a single event to standard format
        """
        try:
            # Parse timestamp
            timestamp_str = event.get('timestamp', '')
            if isinstance(timestamp_str, str):
                # Try multiple date formats
                for fmt in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                    try:
                        timestamp = datetime.strptime(timestamp_str.split('+')[0].split('Z')[0], fmt)
                        break
                    except:
                        continue
                else:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                timestamp = timestamp_str

            return {
                'event_id': event['event_id'],
                'timestamp': timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp,
                'datetime_obj': timestamp if isinstance(timestamp, datetime) else datetime.now(),
                'latitude': float(event['latitude']),
                'longitude': float(event['longitude']),
                'depth_km': float(event['depth_km']),
                'magnitude': float(event['magnitude']),
                'magnitude_type': event['magnitude_type'],
                'location_name': event['location_name'],
                'source': event['source'],
                'region': event.get('region', 'Unknown')
            }
        except Exception as e:
            print(f"Error normalizing event: {e}")
            return None

    def _deduplicate_events(
        self,
        events: List[Dict],
        spatial_threshold_km: float = 10.0,
        time_threshold_minutes: float = 5.0
    ) -> List[Dict]:
        """
        Remove duplicate events from different sources

        Args:
            events: List of events
            spatial_threshold_km: Max distance to consider events as duplicates
            time_threshold_minutes: Max time difference to consider events as duplicates

        Returns:
            Deduplicated event list
        """
        if not events:
            return []

        # Sort by magnitude (descending) to prefer keeping larger events
        events_sorted = sorted(events, key=lambda x: x['magnitude'], reverse=True)

        unique_events = []
        used_indices = set()

        for i, event1 in enumerate(events_sorted):
            if i in used_indices:
                continue

            # Check for duplicates
            duplicates = [event1]

            for j, event2 in enumerate(events_sorted[i+1:], start=i+1):
                if j in used_indices:
                    continue

                # Calculate spatial and temporal distance
                distance_km = self._haversine_distance(
                    event1['latitude'], event1['longitude'],
                    event2['latitude'], event2['longitude']
                )

                time_diff_minutes = abs(
                    (event1['datetime_obj'] - event2['datetime_obj']).total_seconds() / 60
                )

                # If within thresholds, consider as duplicate
                if distance_km <= spatial_threshold_km and time_diff_minutes <= time_threshold_minutes:
                    duplicates.append(event2)
                    used_indices.add(j)

            # Merge duplicates
            if len(duplicates) > 1:
                merged_event = self._merge_duplicate_events(duplicates)
                unique_events.append(merged_event)
            else:
                unique_events.append(event1)

        return unique_events

    def _merge_duplicate_events(self, duplicates: List[Dict]) -> Dict:
        """
        Merge multiple reports of the same event
        """
        # Average coordinates and properties
        merged = duplicates[0].copy()

        merged['latitude'] = sum(e['latitude'] for e in duplicates) / len(duplicates)
        merged['longitude'] = sum(e['longitude'] for e in duplicates) / len(duplicates)
        merged['depth_km'] = sum(e['depth_km'] for e in duplicates) / len(duplicates)
        merged['magnitude'] = sum(e['magnitude'] for e in duplicates) / len(duplicates)

        # Combine sources
        sources = [e['source'] for e in duplicates]
        merged['source'] = 'MERGED' if len(set(sources)) > 1 else sources[0]
        merged['sources_list'] = list(set(sources))

        return merged

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula

        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth radius in kilometers

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def _classify_region(self, lat: float, lon: float) -> str:
        """
        Classify event into a Turkish seismic region

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Region name
        """
        # Check each region (in priority order)
        regions_by_priority = sorted(
            self.REGIONS.items(),
            key=lambda x: x[1]['priority']
        )

        for region_name, region_data in regions_by_priority:
            bbox = region_data['bbox']
            if (bbox['lat_min'] <= lat <= bbox['lat_max'] and
                bbox['lon_min'] <= lon <= bbox['lon_max']):
                return region_name

        return 'Other'

    def detect_patterns(self, events: List[Dict]) -> Dict:
        """
        Detect seismic patterns in event data

        Returns:
            Dictionary containing detected patterns
        """
        patterns = {
            'temporal': self._detect_temporal_patterns(events),
            'spatial': self._detect_spatial_clusters(events),
            'anomalies': self._detect_anomalies(events)
        }

        return patterns

    def _detect_temporal_patterns(self, events: List[Dict]) -> List[Dict]:
        """
        Detect temporal patterns like swarms and sequences
        """
        if not events:
            return []

        patterns = []

        # Sort by time
        sorted_events = sorted(events, key=lambda x: x['datetime_obj'])

        # Detect rapid sequences (>5 events within 24 hours)
        time_windows = defaultdict(list)

        for event in sorted_events:
            window_key = event['datetime_obj'].strftime('%Y-%m-%d')
            time_windows[window_key].append(event)

        for date, day_events in time_windows.items():
            if len(day_events) >= 5:
                max_mag = max(e['magnitude'] for e in day_events)
                patterns.append({
                    'type': 'rapid_sequence',
                    'date': date,
                    'event_count': len(day_events),
                    'max_magnitude': max_mag,
                    'description': f'{len(day_events)} events on {date}, max M{max_mag:.1f}'
                })

        # Detect potential foreshock-mainshock-aftershock sequences
        # Find events M >= 4.0 and check for activity before/after
        significant_events = [e for e in sorted_events if e['magnitude'] >= 4.0]

        for mainshock in significant_events:
            mainshock_time = mainshock['datetime_obj']

            # Check for foreshocks (24h before)
            foreshocks = [
                e for e in sorted_events
                if e['datetime_obj'] < mainshock_time
                and (mainshock_time - e['datetime_obj']).total_seconds() < 86400
                and self._haversine_distance(
                    e['latitude'], e['longitude'],
                    mainshock['latitude'], mainshock['longitude']
                ) < 50
            ]

            # Check for aftershocks (72h after)
            aftershocks = [
                e for e in sorted_events
                if e['datetime_obj'] > mainshock_time
                and (e['datetime_obj'] - mainshock_time).total_seconds() < 259200
                and self._haversine_distance(
                    e['latitude'], e['longitude'],
                    mainshock['latitude'], mainshock['longitude']
                ) < 50
            ]

            if len(aftershocks) >= 3:
                patterns.append({
                    'type': 'mainshock_sequence',
                    'mainshock': {
                        'magnitude': mainshock['magnitude'],
                        'time': mainshock['timestamp'],
                        'location': mainshock['location_name']
                    },
                    'foreshock_count': len(foreshocks),
                    'aftershock_count': len(aftershocks),
                    'description': f'M{mainshock["magnitude"]:.1f} mainshock with {len(aftershocks)} aftershocks'
                })

        return patterns

    def _detect_spatial_clusters(self, events: List[Dict]) -> List[Dict]:
        """
        Detect spatial clustering of events
        """
        if len(events) < 5:
            return []

        clusters = []

        # Simple density-based clustering
        # Group events within 20km radius
        used = set()

        for i, event in enumerate(events):
            if i in used:
                continue

            cluster_events = [event]
            used.add(i)

            for j, other_event in enumerate(events):
                if j in used or j == i:
                    continue

                distance = self._haversine_distance(
                    event['latitude'], event['longitude'],
                    other_event['latitude'], other_event['longitude']
                )

                if distance < 20:  # 20km radius
                    cluster_events.append(other_event)
                    used.add(j)

            # Only report clusters with 5+ events
            if len(cluster_events) >= 5:
                center_lat = sum(e['latitude'] for e in cluster_events) / len(cluster_events)
                center_lon = sum(e['longitude'] for e in cluster_events) / len(cluster_events)
                max_mag = max(e['magnitude'] for e in cluster_events)

                clusters.append({
                    'event_count': len(cluster_events),
                    'center_lat': center_lat,
                    'center_lon': center_lon,
                    'max_magnitude': max_mag,
                    'region': self._classify_region(center_lat, center_lon),
                    'description': f'Cluster of {len(cluster_events)} events near ({center_lat:.2f}, {center_lon:.2f})'
                })

        return clusters

    def _detect_anomalies(self, events: List[Dict]) -> List[Dict]:
        """
        Detect anomalous patterns
        """
        anomalies = []

        if not events:
            return anomalies

        # Anomaly: Unusually shallow events (< 5km)
        shallow_events = [e for e in events if e['depth_km'] < 5]
        if len(shallow_events) >= 3:
            anomalies.append({
                'type': 'shallow_depth',
                'count': len(shallow_events),
                'description': f'{len(shallow_events)} unusually shallow events (< 5km depth)'
            })

        # Anomaly: Unusual magnitude for region
        istanbul_events = [e for e in events if e['region'] == 'Istanbul']
        large_istanbul = [e for e in istanbul_events if e['magnitude'] >= 4.0]
        if large_istanbul:
            anomalies.append({
                'type': 'significant_magnitude',
                'region': 'Istanbul',
                'count': len(large_istanbul),
                'max_magnitude': max(e['magnitude'] for e in large_istanbul),
                'description': f'{len(large_istanbul)} M≥4.0 events in Istanbul region'
            })

        return anomalies

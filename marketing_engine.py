"""
Chamunda Automobile Parts & Service - Royal Enfield Growth & Marketing Engine.
Orchestrates YouTube Shorts campaigns, customer acquisition, and brand dominance for Royal Enfield parts.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.youtube_commander import YouTubeShortsCommander
from tools.laptop_work_tools import send_desktop_notification
from omnichannel_social_engine import ChamundaOmnichannelSocialEngine


RE_VIRAL_CAMPAIGNS = [
    {
        "topic": "Royal Enfield Classic 350 Cold Start Tappet Noise Fix",
        "niche": "Motorcycle Maintenance & Royal Enfield Tuning",
        "hook": "Why does your Royal Enfield sound like a sewing machine on cold morning starts?"
    },
    {
        "topic": "Top 3 Engine Oil Mistakes that destroy Royal Enfield 650 Twins",
        "niche": "Motorcycle Maintenance & Royal Enfield Tuning",
        "hook": "Using the wrong oil in your Interceptor 650 can fry your clutch plates!"
    },
    {
        "topic": "Himalayan 450 Long Ride Pre-Trip Maintenance Checklist",
        "niche": "Motorcycle Touring & Adventure Preparation",
        "hook": "Before your Ladakh trip, check these 4 critical items on your Himalayan 450!"
    },
    {
        "topic": "Hunter 350 Mileage & Smooth Throttle Tuning Secret",
        "niche": "Motorcycle Tuning & Performance",
        "hook": "How to get buttery smooth gear shifts and +5 km/l on your Hunter 350."
    }
]


class ChamundaMarketingEngine:
    """Automates brand marketing, YouTube Shorts, and 360° Omnichannel social campaigns."""

    def __init__(self):
        self.yt_commander = YouTubeShortsCommander()
        self.social_engine = ChamundaOmnichannelSocialEngine()

    def launch_re_marketing_short(self, campaign_index: int = 0, custom_topic: Optional[str] = None) -> Dict[str, Any]:
        """Trigger autonomous creation of a Royal Enfield marketing Short via the subordinate YouTube agent."""
        if custom_topic:
            topic = custom_topic
            niche = "Royal Enfield Service & Spares"
        else:
            campaign = RE_VIRAL_CAMPAIGNS[campaign_index % len(RE_VIRAL_CAMPAIGNS)]
            topic = campaign["topic"]
            niche = campaign["niche"]

        result = self.yt_commander.run_and_supervise_pipeline(
            niche=niche,
            topic=topic,
            dry_run=False
        )
        return result

    def launch_omnichannel_campaign(self, topic: str, channels: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate and syndicate a 360° campaign across WhatsApp, Instagram, Facebook, Google Business, and YouTube."""
        campaign = self.social_engine.generate_multi_platform_campaign(topic=topic)
        pub_result = self.social_engine.publish_to_channels(campaign_data=campaign, target_channels=channels)
        return {
            "campaign": campaign,
            "publication": pub_result
        }


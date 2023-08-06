# brightrolladclient
Client for the Brightroll Ad DSP

Sample code:


from brightrolladclient import BrightRollClient
client = BrightRollClient()
client.show_config()
client.set_payload()
client.encode_payload()
client.set_oauth_url()
client.set_payload_url()
client.set_headers()
client.get_token()
client.get_organizations()
client.get_campaigns(org_id)
client.get_campaigns_by_advertiser(org_id, ad_id)
client.get_campaigns_by_advertiser_by_campaign(org_id, ad_id, campaign_id)


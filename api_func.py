import time

from goplus.token import Token
import requests
import json


def send_to_go_plus(token_address):
    score = 0
    counter = 14
    array_of_errors = []
    try:
        data = Token(access_token=None).token_security(chain_id="1", addresses=[token_address.lower()])
        security = data.result[f'{token_address.lower()}']

        transferable_pause = str(security.transfer_pausable)
        lp_count = str(security._lp_holder_count)
        hidden_owner = str(security._hidden_owner)
        whitelised = str(security._is_whitelisted)
        #print(whitelised)
        anti_whale = str(security._is_anti_whale)
        blacklisted = str(security._is_blacklisted)
        honeypot = str(security._is_honeypot)
        dex = str(security._is_in_dex)
        mintable = str(security._is_mintable)
        opensource = str(security._is_open_source)
        proxy = str(security._is_proxy)
        true_token = str(security._is_true_token)
        other = security._other_potential_risks




        #print(security)
        #print(int((security._is_honeypot)) + 1)

        while (counter > 0):
            if counter == 14:
                if transferable_pause != None or transferable_pause != '0':
                    array_of_errors.append(f"Transferable pause = {transferable_pause}")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 13:
                if lp_count != None or lp_count != '0':
                    array_of_errors.append(f"Security has {lp_count} LP Count Holders")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 12:
                if hidden_owner == '1':
                    score += 1
                    array_of_errors.append("Security has hidden owner")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 11:
                if whitelised == '1':
                    score += 1
                    array_of_errors.append("security is whitelisted")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 10:
                if anti_whale == '1':
                    score += 1
                    array_of_errors.append("security is anti whale")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 9:
                if blacklisted == '1':
                    score += 1
                    array_of_errors.append("security is blacklisted")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 8:
                if honeypot == '1':
                    score += 1
                    array_of_errors.append("security is honeypot")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 7:
                if dex == 1:
                    score += 1
                    array_of_errors.append("security is in dex")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 6:
                if mintable == '1':
                    score += 1
                    array_of_errors.append("security is mintable")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 5:
                if opensource == '1':
                    score += 1
                    array_of_errors.append("security is open source")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 4:
                if proxy == 1:
                    score += 1
                    array_of_errors.append("security is proxy")
                    counter -= 2
                else:
                    counter -= 2
            elif counter == 2:
                if true_token == '1':
                    score += 1
                    array_of_errors.append("security is a true token")
                    counter -= 1
                else:
                    counter -= 1
            elif counter == 1:
                if security._other_potential_risks != 'None':
                    score += 1
                    array_of_errors.append("Other Potential Risks")
                    counter -= 1
                else:
                    counter -= 1

        print(f"{score} / 11")
        print(f"\n Errors:\n{array_of_errors}")

        overall = f'{score}/11\n Errors:\n {array_of_errors}'

        return overall

    except Exception as e:
        print(f"Failed to send to Go+ Security. Error: {str(e)}")



def get_token_sniffer_score(token_address, api):
    base_url = "https://tokensniffer.com/api/v2/tokens"
    url = f"{base_url}/1/{token_address}?apikey={api}"
    headers = {"accept": "application/json"}
    params = {
        'include_metrics': 'true',
    }

    response = requests.get(url, headers=headers, params=params)

    # Check if the response status code is 200 (HTTP OK)
    if response.status_code != 200:
        print("Not found in database")
        return None

    try:
        end_p = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Not found in database")
        return None

    score_ts = end_p.get('score', None)  # Use .get() to avoid KeyError in case 'score' is not in the response

    if score_ts is not None:
        print(f"The score for Token Sniffer is {score_ts}")
        return score_ts
    else:
        time.sleep(5)
        response2 = requests.get(url, headers=headers, params=params)
        end_p2 = json.loads(response2.text)
        score_tss = end_p2.get('score', None)
        if score_tss is not None:
            print(f"The score for Token Sniffer is {score_tss}")
            return score_tss
        else:
            print("Score not found in the response")
            return score_tss

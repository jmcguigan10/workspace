from typing import Any, Dict, List

from AI_vendor.utils.api_utils import Get_Provider
from AI_vendor.utils.input_utils import Input_Provider
from AI_vendor.utils.output_utils import Provider_Output


class OpenAIChatProvider:
    def __init__(self):
        self.out_url = Get_Provider.get_out_url()
        self.api_key = Get_Provider.get_api_key()

    def generate_json(
        self,
        message: List[Dict[str, str]],
        args,
    ) -> Dict[str, Any]:
        payload = Input_Provider.get_message(message, args)

        timeout = 120
        pre_data = Provider_Output.get_output(
            payload, self.out_url, self.api_key, timeout
        )
        data = Provider_Output.get_text(pre_data)
        clean_json = Provider_Output.get_clean_json(data)

        return clean_json

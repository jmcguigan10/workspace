from AI_assistant.AI_vendor.oai import OpenAIChatProvider
from AI_assistant.AI_vendor.utils._ProviderError import ProviderError


def get_provider(input):
    name = input["provider_name"]
    if name == "openai_chat":
        return OpenAIChatProvider()
    """
    if name == "openai_compatible":
        return OpenAICompatibleProvider()
    if name == "anthropic_messages":
        return AnthropicMessagesProvider()
    """
    raise ProviderError(
        f"Unknown provider '{name}'. Choose: openai_chat | openai_compatible | anthropic_messages"
    )

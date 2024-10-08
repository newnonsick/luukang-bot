import google.generativeai as genai

class Utils:
    @staticmethod
    async def upload_to_gemini(path, mime_type=None):
        """Uploads the given file to Gemini.

        See https://ai.google.dev/gemini-api/docs/prompting_with_media
        """
        print(f"Uploading file '{path}' to Gemini...")
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")

        return file

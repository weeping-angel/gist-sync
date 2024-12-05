import json
from pathlib import Path
import typing as t

import requests


class GISTAmbiguityError(Exception):
    def __init__(self, gist_ids_list: t.List[str], message: str = "Number of GIST IDs is too ambiguous") -> None:
        self.gist_ids_list = gist_ids_list
        self.message = message

        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}\nIDs: " + ", ".join(self.gist_ids_list)


class GistSync:
    def __init__(self, auth_token: str) -> None:
        self.auth_token = auth_token
        self._headers = {"Authorization": f"token {auth_token}"}

    @staticmethod
    def _readnparse_python_file(file_name: t.Union[Path, str], sep: str = "#%%") -> t.Dict[t.Any, t.Any]:
        codelines = open(Path(file_name), 'r').readlines()
        filename, extension = file_name.name.split('.')

        if extension in ['py', 'sh']:
            snippet_count = 0
            snippets = ['']

            metadata=  ''
            for line in codelines:
                if '#-- title:' in line:
                    title = line.replace('#-- title:', '').strip()
                    metadata += f'[{title}] '
                elif '#-- description:' in line:
                    description = line.replace('#-- description:', '').strip()
                    metadata += f'{description} '
                elif '#-- tags:' in line:
                    tags = line.replace('#-- tags:', '').strip()
                    metadata += ' '.join([f'#{tag.strip()}' for tag in tags.split(',')])
                elif '#%%' in line:
                    snippet_count += 1
                    snippets.append('')
                else:
                    snippets[snippet_count] += line

            gist_code_dict = {
                file_name.name: {"content": '\n\n'.join([i.strip('\n') for i in snippets])},
            }

            if len(snippets) > 1:
                for index, snippet in enumerate(snippets):
                    gist_code_dict[f"{filename}_{index+1}.{extension}"] = {"content": snippet.strip('\n')}

            try:
                output_filename = f"{filename}_output.txt"
                output_filepath = f"{file_name.parent}/{output_filename}"

                output = open(Path(output_filepath), 'r').read()

                gist_code_dict[output_filename] = {"content": output.strip('\n')}

            except Exception as e:
                print("No output file found")

            data = {
                "public": True,
                "description": metadata,
                "files": gist_code_dict,
            }

            return data
        
        elif extension in ['js']:
            gist_code_dict = {
                file_name.name: {"content": '\n'.join([i.strip('\n') for i in codelines])},
            }
            try:
                output_filename = f"{filename}_output.txt"
                output_filepath = f"{file_name.parent}/{output_filename}"

                output = open(Path(output_filepath), 'r').read()

                gist_code_dict[output_filename] = {"content": output.strip('\n')}

            except Exception as e:
                print("No output file found")

            data = {
                "public": True,
                "files": gist_code_dict,
            }

            return data
        
        else:
            return {
                "public": True,
                "files": {
                    file_name.name: open(Path(file_name), 'r').read()
                }
            }

        

    def _get_gist_id(self, file_name: t.Optional[Path] = None, gist_id: t.Optional[str] = None) -> str:
        if isinstance(gist_id, str):
            gist_id_ret = gist_id

        elif isinstance(file_name, Path):
            gist_ids = [gist['id'] for gist in self.get_gists() if file_name.name in gist['files']]
            if len(set(gist_ids)) > 1:
                raise GISTAmbiguityError(gist_ids_list=gist_ids)

            gist_id_ret = gist_ids[0]

        return gist_id_ret

    def get_gists(self) -> t.List[t.Dict]:
        def _get_gists_resp(page_no=0):
            url = f"https://api.github.com/gists?page={page_no}&per_page=100"
            resp = requests.get(url, headers=self._headers)
            return resp

        gists = []

        i = 0
        resp = _get_gists_resp(i)
        resp_json = resp.json()

        while resp_json and resp.status_code!=401:
            gists.extend(resp_json)
            
            i += 1
            resp = _get_gists_resp(page_no=i)
            resp_json = resp.json()

        return gists

    def create_gist(self, file_name: t.Union[Path, str], sep: str = "#%%") -> t.List:
        _query_url = "https://api.github.com/gists"

        rest_api_data = self._readnparse_python_file(file_name, sep=sep)

        resp = requests.post(_query_url, headers=self._headers, data=json.dumps(rest_api_data))
        resp_data = resp.json()

        return resp_data

    def update_gist(self, file_name: t.Union[Path, str], gist_id: t.Optional[str] = None) -> t.List:
        file_name = Path(file_name)

        gist_id = self._get_gist_id(file_name=file_name, gist_id=gist_id)

        _query_url = f"https://api.github.com/gists/{gist_id}"

        rest_api_data = self._readnparse_python_file(file_name)

        resp = requests.patch(_query_url, headers=self._headers, data=json.dumps(rest_api_data))
        resp_data = resp.json()

        return resp_data

    def delete_gist(self, file_name: t.Optional[t.Union[Path, str]] = None, gist_id: t.Optional[str] = None) -> int:
        if file_name:
            file_name = Path(file_name)
            gist_id = self._get_gist_id(file_name=file_name, gist_id=gist_id)

        _query_url = f"https://api.github.com/gists/{gist_id}"

        resp = requests.delete(_query_url, headers=self._headers)
        resp_status = resp.status_code

        return resp_status

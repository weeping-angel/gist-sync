import json
from pathlib import Path
import typing as t

import requests


class GISTAmbiguityError(Exception):
    def __init__(
        self, gist_ids_list: t.List[str], message: str = "Number of GIST IDs is too ambiguous"
    ) -> None:
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
    def _readnparse_python_file(
        file_name: t.Union[Path, str], sep: str = "#%%"
    ) -> t.Dict[t.Any, t.Any]:

        file_name = Path(file_name)

        with open(file_name, "r") as file_obj:
            file_content = file_obj.read()

        core_file_name = file_name.name

        file_content_list = file_content.split(f"{sep}\n")

        gist_code_dict = {}

        for index, k in enumerate(file_content_list):
            if index == 0:
                gist_code_dict[core_file_name] = {"content": k}

            else:
                gist_code_dict[core_file_name.replace(".py", f"_{index}.py")] = {"content": k}

        data = {
            "public": True,
            "files": gist_code_dict,
        }

        return data

    def _get_gist_id(
        self, file_name: t.Optional[Path] = None, gist_id: t.Optional[str] = None
    ) -> str:
        if isinstance(gist_id, str):
            gist_id_ret = gist_id

        elif isinstance(file_name, Path):
            gist_ids = []
            gist_list = self.get_gists()

            for _gist in gist_list:
                if file_name.name in _gist["files"]:
                    gist_ids.append(_gist["id"])

            if len(gist_ids) > 1:
                raise GISTAmbiguityError(gist_ids_list=gist_ids)

            gist_id_ret = gist_ids[0]

        return gist_id_ret

    def get_gists(self) -> t.List[t.Dict]:
        _query_url = "https://api.github.com/gists?page=PAGE&per_page=100"
        resp_data = []
        cntr = 0
        _resp_ansr = True
        while _resp_ansr:
            cntr += 1

            resp = requests.get(_query_url.replace("PAGE", str(cntr)), headers=self._headers)
            resp_content = resp.json()

            if len(resp_content) > 0:
                resp_data.extend(resp_content)

            else:
                _resp_ansr = False

        return resp_data

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

    def delete_gist(
        self, file_name: t.Optional[t.Union[Path, str]] = None, gist_id: t.Optional[str] = None
    ) -> int:
        if file_name:
            file_name = Path(file_name)
            gist_id = self._get_gist_id(file_name=file_name, gist_id=gist_id)

        _query_url = f"https://api.github.com/gists/{gist_id}"

        resp = requests.delete(_query_url, headers=self._headers)
        resp_status = resp.status_code

        return resp_status

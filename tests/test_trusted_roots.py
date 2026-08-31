import os
import unittest
from pathlib import Path
from unittest.mock import patch

import mcp_server


class TrustedRootsTests(unittest.TestCase):
    def test_strict_root_allows_child_and_rejects_external_path(self):
        env = {
            mcp_server.ENV_WORKSPACE_ROOT: r"D:\Youtube",
            mcp_server.ENV_TRUSTED_ROOTS: r"D:\Youtube",
            mcp_server.ENV_INCLUDE_AGY_TRUSTED_ROOTS: "0",
        }
        settings = {"trustedWorkspaces": [r"C:\Users\Administrator"]}

        with patch.dict(os.environ, env, clear=False), patch.object(
            mcp_server, "_read_json", return_value=settings
        ):
            mcp_server._validate_workspace_path(
                Path(r"D:\Youtube\ExampleChannel"), "cwd"
            )
            with self.assertRaisesRegex(
                ValueError,
                r"cwd must be inside a trusted workspace.*D:\\Youtube",
            ):
                mcp_server._validate_workspace_path(
                    Path(r"C:\Users\Administrator\OtherProject"), "cwd"
                )


if __name__ == "__main__":
    unittest.main()

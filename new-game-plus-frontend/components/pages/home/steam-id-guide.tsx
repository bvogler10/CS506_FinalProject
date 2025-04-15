import { Card, CardContent } from "@/components/ui/card";

export default function SteamIdGuide() {
  return (
    <div className="grid gap-8 md:grid-cols-2">
      <Card>
        <CardContent className="p-6">
          <h3 className="text-xl font-bold mb-4">
            Method 1: From Your Profile URL
          </h3>
          <ol className="space-y-4 text-gray-200">
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                1
              </span>
              <span>
                Log in to your Steam account and click on your profile name in
                the top navigation bar.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                2
              </span>
              <span>
                Look at the URL in your browser's address bar. It will look
                something like:
              </span>
            </li>
            <li className="bg-gray-900 p-3 rounded text-gray-400 font-mono text-sm break-all">
              https://steamcommunity.com/id/[custom-url]/
              <br />
              or
              <br />
              https://steamcommunity.com/profiles/[17-digit-number]/
            </li>
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                3
              </span>
              <span>
                If your URL has "profiles" followed by a 17-digit number, that
                number is your Steam ID.
              </span>
            </li>
          </ol>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-6">
          <h3 className="text-xl font-bold mb-4">
            Method 2: From Steam Client
          </h3>
          <ol className="space-y-4 text-gray-200">
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                1
              </span>
              <span>
                Open the Steam client and click on your username in the
                top-right corner.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                2
              </span>
              <span>Select "Account Details" from the dropdown menu.</span>
            </li>
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                3
              </span>
              <span>
                Your Steam ID will be displayed on this page, usually in the
                format: STEAM_X:Y:ZZZZZZ
              </span>
            </li>
            <li className="flex gap-2">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-secondary text-sm font-bold">
                4
              </span>
              <span>
                Alternatively, you can use a third-party website like{" "}
                <a
                  href="https://steamid.io"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-secondary hover:underline"
                >
                  SteamID.io
                </a>{" "}
                to convert between different Steam ID formats.
              </span>
            </li>
          </ol>
        </CardContent>
      </Card>
    </div>
  );
}

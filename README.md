# Yacht Alpha

For alpha testing, you can start yacht with the following command:

```bash
docker run -d \
    --name ayacht \ #or whatever name you want
    -p 3000:3000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    ghcr.io/selfhostedpro/yacht-nuxt:main
```

if you'd like persistent configs you can run this instead:

```bash
docker run -d \
    --name ayacht \ #or whatever name you want
    -p 3000:3000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /path/to/config/dir/or/volume/name:/config \ # for yacht config directory
    -v /path/to/data/dir/or/volume/name:/data \ # for yacht project/data directory
    ghcr.io/selfhostedpro/yacht-nuxt:main
```

you can remove yacht with the following command:

```bash
docker rm -f ayacht # or whatever name you set above
```

Look at the [Nuxt 3 documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install the dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm run dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm run build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm run preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

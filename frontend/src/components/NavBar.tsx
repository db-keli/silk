export default function NavBar() {
  return (
    <>
      <nav className=" flex flex-row justify-center">
        <svg
          href="./logo.jpg"
          className="basis-1/5 rounded-full"
          width="200"
          height="200"
          xmlns="http://www.w3.org/2000/svg"
        >
          <image
            height="100%"
            width="100%"
            href="https://comicvine.gamespot.com/a/uploads/scale_small/11/111746/5120797-aristidefiloselle_c1033a1.jpg"
          />
        </svg>
        <p className="text-white basis-3/5 text-center mt-11 text-5xl">
          Grab the youtube videos
        </p>
        <div className="text-white basis-1/5 text-center">
          <ul>
            <li>Playlists</li>
            <li>Singles</li>
          </ul>
        </div>
      </nav>
    </>
  );
}

export default function NavBar() {
  return (
    <>
      <nav className=" flex flex-row justify-center">
        <svg
          href="./logo.jpg"
          className=" max-sm:w-auto basis-1/5 flex flex-row justify-center"
          width="200"
          height="200"
          xmlns="http://www.w3.org/2000/svg"
        >
          <image height="200" width="200" href="/logo.jpg" />
        </svg>
        <p className="text-white basis-3/5 text-center mt-11 text-5xl">Silk</p>
        <div className="text-white basis-1/5 text-center">
          <ul>
            <li className="text-left">Playlists</li>
            <li className="text-left">Singles</li>
          </ul>
        </div>
      </nav>
    </>
  );
}

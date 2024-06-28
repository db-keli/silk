export default function NavBar() {
  return (
    <>
      <nav className="fixed top-1 w-full left-0 ">
        <div className="flex flex-row justify-between ">
          <div className="basis-1/4" />
          <svg
            width="60"
            height="60"
            xmlns="http://www.w3.org/2000/svg"
            className="basis-1/4 flex flex-row justify-center"
          >
            <image href="../../public/vite.svg" height="50" width="50" />
          </svg>
          <div className="basis-1/4 flex flex-row">
            <text className=" text-white basis-1/12 mt-4 text-3xl">Home</text>
          </div>
          <div className="basis-1/4" />
        </div>
      </nav>
    </>
  );
}

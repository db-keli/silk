export default function Preview() {
  return (
    <div className="flex flex-row mt-5">
      <div className="basis-2/12" />
      <svg className="basis-3/12">
        <image
          href="https://i.ytimg.com/vi/CH50zuS8DD0/hq720.jpg"
          height={"100%"}
          width={"100%"}
        />
      </svg>
      <div className="basis-5/12 text-white ml-2">
        <p className="text-lg">1 Minute Timer</p>
        <p>4:5</p>
      </div>
    </div>
  );
}

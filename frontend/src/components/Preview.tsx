type Props = {
  thumbnailLink: string;
  title: string;
};

export default function Preview(prop: Props) {
  return (
    <div className="flex flex-row mt-9">
      <div className="basis-2/12" />
      <svg className="basis-3/12">
        <image href={prop.thumbnailLink} height={"100%"} width={"100%"} />
      </svg>
      <div className="basis-5/12 text-white ml-2">
        <p className="mt-2">{prop.title}</p>
      </div>
    </div>
  );
}

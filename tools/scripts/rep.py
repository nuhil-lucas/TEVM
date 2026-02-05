from pylucas.tool import ReleasePacker


if __name__ == "__main__":
    REP: ReleasePacker = ReleasePacker(name="TEVM", output="./dist/TEVM")
    REP.build()
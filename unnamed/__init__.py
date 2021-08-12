class SemVer:
    __slots__ = ("major", "minor", "patch", "release")

    def __init__(self, major, minor, patch, release=None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.release = release.lower()

    @property
    def numerical_string(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __str__(self):
        return f"{self.numerical_string}-{self.release}"


VERSION = SemVer(0, 1, 0, "alpha")

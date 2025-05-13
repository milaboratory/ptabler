import typing
import msgspec
import polars as pl
import polars_hash as plh

from .base import Expression

# Define type literals based on the TypeScript definitions
HashType = typing.Literal[
    'sha256',  # Cryptographic
    'sha512',  # Cryptographic
    'md5',     # Cryptographic (use with caution)
    'blake3',  # Cryptographic
    'wyhash',  # Non-cryptographic
    'xxh3',    # Non-cryptographic
]

HashEncoding = typing.Literal['hex', 'base64']

_CRYPTOGRAPHIC_HASH_TYPES: set[HashType] = {
    'sha256', 'sha512', 'md5', 'blake3'}
_NON_CRYPTOGRAPHIC_HASH_TYPES: set[HashType] = {
    'wyhash', 'xxh3'
}


class HashExpression(Expression, tag='hash', tag_field="type", rename="camel"):
    """
    Represents a hashing operation on an expression's value.

    Corresponds to the HashExpression interface in TypeScript. It uses the
    polars-hash library for underlying computations.
    """
    hash_type: HashType
    """The specific hash algorithm to apply (e.g., 'sha256', 'wyhash')."""

    encoding: HashEncoding
    """The desired string encoding for the output hash ('hex' or 'base64')."""

    value: Expression
    """The expression whose resulting value will be hashed."""

    def to_polars(self) -> pl.Expr:
        """
        Converts the hash expression definition into a Polars expression.

        Handles different hash types (cryptographic vs. non-cryptographic)
        and desired output encodings.

        Raises:
            NotImplementedError: If base64 encoding is requested for hash types
                                 where it's not currently supported or straightforward
                                 to implement via polars-hash/Polars directly.
            AttributeError: If the specified hash_type is not supported by the
                            polars-hash library accessor (.chash or .nchash).
            ValueError: If an unknown hash_type is encountered (should not happen
                        with Literal typing).
        """
        polars_value = self.value.to_polars()

        if self.hash_type in _CRYPTOGRAPHIC_HASH_TYPES:
            try:
                # Access the appropriate cryptographic hasher, e.g., polars_value.chash.sha256
                hasher = getattr(polars_value.chash, self.hash_type)
            except AttributeError:
                raise AttributeError(
                    f"Cryptographic hash type '{self.hash_type}' not supported by polars-hash .chash accessor."
                )

            # Assume the hasher() call returns a hex-encoded string expression
            hashed_expr = hasher()

            if self.encoding == 'base64':
                return hashed_expr.str.decode('hex').bin.encode('base64')
            elif self.encoding == 'hex':
                return hashed_expr
            else:
                raise ValueError(
                    f"Unsupported encoding for cryptographic hash: {self.encoding}")

        elif self.hash_type in _NON_CRYPTOGRAPHIC_HASH_TYPES:
            try:
                hasher = getattr(polars_value.nchash, self.hash_type)
            except AttributeError:
                raise AttributeError(
                    f"Non-cryptographic hash type '{self.hash_type}' not supported by polars-hash .nchash accessor."
                )

            # These hashers return a pl.UInt64 expression
            hashed_expr_u64 = hasher()

            if self.encoding == 'hex':
                return hashed_expr_u64.format("{:x}")
            elif self.encoding == 'base64':
                raise NotImplementedError(
                    f"Base64 encoding is not currently supported for non-cryptographic hash type '{self.hash_type}'."
                )
            else:
                raise ValueError(
                    f"Unsupported encoding for non-cryptographic hash: {self.encoding}")

        else:
            raise ValueError(f"Unknown hash type: {self.hash_type}")
